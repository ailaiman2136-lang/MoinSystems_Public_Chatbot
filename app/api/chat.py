import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.chat import ChatSession, ChatMessage
from app.services.chat_service import generate_answer

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[str]
    lead_capture_required: bool


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    session_id = request.session_id or uuid.uuid4().hex

    chat_session = db.scalar(
        select(ChatSession).where(
            ChatSession.session_id == session_id
        )
    )

    if not chat_session:
        chat_session = ChatSession(session_id=session_id)
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

    previous_messages = db.scalars(
        select(ChatMessage)
        .where(ChatMessage.session_id == chat_session.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(10)
    ).all()

    history = [
        {"role": item.role, "content": item.content}
        for item in reversed(previous_messages)
    ]

    db.add(ChatMessage(
        session_id=chat_session.id,
        role="user",
        content=request.message
    ))
    db.commit()

    try:
        answer, sources = generate_answer(request.message, history)
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"AI response generation failed: {str(error)}"
        )

    db.add(ChatMessage(
        session_id=chat_session.id,
        role="assistant",
        content=answer
    ))
    db.commit()

    message_lower = request.message.lower()

    lead_keywords = [
        "price", "pricing", "quote", "estimate", "project",
        "hire", "contact", "work with you"
    ]

    lead_required = any(
        keyword in message_lower for keyword in lead_keywords
    )

    return ChatResponse(
        session_id=session_id,
        answer=answer,
        sources=sources,
        lead_capture_required=lead_required
    )