import math
from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.knowledge import KnowledgeDocument
from app.services.embedding_service import generate_query_embedding

TOP_K = 5
MIN_SIMILARITY = 0.40

INTENT_RULES = {
    "pricing": {
        "keywords": ["price", "pricing", "cost", "quote", "estimate", "budget"],
        "boosts": {"pricing": 0.15, "quote_request": 0.15}
    },
    "lead_capture": {
        "keywords": [
            "start a project", "contact me", "get in touch",
            "hire", "work with you"
        ],
        "boosts": {"lead_capture": 0.20, "human_handoff": 0.10}
    },
    "email": {
        "keywords": [
            "send my project", "send project information",
            "send my information", "send to your team",
            "email your team"
        ],
        "boosts": {"lead_notification": 0.25, "human_handoff": 0.10}
    }
}


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))

    if not norm_a or not norm_b:
        return 0.0

    return dot / (norm_a * norm_b)


def get_intent_boost(query, intents):
    query = query.lower()
    intents = intents or []
    boost = 0.0

    for rule in INTENT_RULES.values():
        if any(word in query for word in rule["keywords"]):
            for intent, value in rule["boosts"].items():
                if intent in intents:
                    boost = max(boost, value)

    return boost


def retrieve_documents(query, top_k=TOP_K):
    session = SessionLocal()

    try:
        query_vector = generate_query_embedding(query.strip())

        documents = session.scalars(
            select(KnowledgeDocument).where(
                KnowledgeDocument.embedding.is_not(None)
            )
        ).all()

        results = []

        for doc in documents:
            similarity = cosine_similarity(query_vector, doc.embedding)

            if similarity < MIN_SIMILARITY:
                continue

            boost = get_intent_boost(query, doc.intents)

            results.append({
                "id": doc.document_id,
                "title": doc.title,
                "content": doc.content,
                "category": doc.category,
                "score": round(similarity + boost, 4),
                "similarity": round(similarity, 4)
            })

        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:top_k]

    finally:
        session.close()