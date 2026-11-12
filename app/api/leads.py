
import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.lead import Lead
from app.services.email_service import send_lead_notification

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LeadRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: str = Field(min_length=5, max_length=255)
    phone: str = Field(min_length=7, max_length=30)
    company: str | None = Field(default=None, max_length=150)
    project_details: str | None = None


@router.post("/leads")
def submit_lead(request: LeadRequest, db: Session = Depends(get_db)):
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", request.email):
        raise HTTPException(status_code=422, detail="Invalid email address")

    lead = Lead(
        full_name=request.full_name,
        email=request.email,
        phone=request.phone,
        company=request.company,
        project_details=request.project_details
    )

    try:
        db.add(lead)
        db.commit()
        db.refresh(lead)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lead could not be saved.")

    notification_sent = False

    try:
        send_lead_notification(lead)
        notification_sent = True
    except Exception as error:
        print(f"Email notification failed: {error}")

    return {
        "message": "Lead submitted successfully.",
        "lead_id": lead.id,
        "notification_sent": notification_sent
    }
