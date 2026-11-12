
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from sqlalchemy import select
from app.db.database import SessionLocal
from app.models.knowledge import KnowledgeDocument
from app.services.embedding_service import generate_embeddings


def main():
    with open(BASE_DIR / "data/knowledge_base.jsonl", encoding="utf-8") as file:
        records = [json.loads(line) for line in file if line.strip()]

    text_by_id = {}

    for record in records:
        parts = [
            f"Title: {record.get('title', '')}",
            f"Category: {record.get('category', '')}",
            f"Tags: {', '.join(record.get('tags', []))}",
            f"Intents: {', '.join(record.get('intents', []))}",
            f"Content: {record.get('embedding_text') or record.get('content', '')}"
        ]
        text_by_id[record["id"]] = "\n".join(parts)

    session = SessionLocal()

    try:
        documents = session.scalars(
            select(KnowledgeDocument)
        ).all()

        print("Knowledge records:", len(documents))

        for start in range(0, len(documents), 10):
            batch = documents[start:start + 10]

            texts = [text_by_id[doc.document_id] for doc in batch]
            vectors = generate_embeddings(texts)

            for doc, vector in zip(batch, vectors):
                doc.embedding = vector

            session.commit()
            print(f"Processed {min(start + 10, len(documents))}/{len(documents)}")

        print("All document embeddings updated successfully!")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
