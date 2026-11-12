
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from sqlalchemy import select
from app.db.database import SessionLocal
from app.models.knowledge import KnowledgeDocument

DATA_FILE = BASE_DIR / "data" / "knowledge_base.jsonl"


def ingest():
    session = SessionLocal()
    inserted = 0
    updated = 0

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                record = json.loads(line)

                existing = session.scalar(
                    select(KnowledgeDocument).where(
                        KnowledgeDocument.document_id == record["id"]
                    )
                )

                values = {
                    "title": record["title"],
                    "category": record["category"],
                    "content": record["content"],
                    "tags": record["tags"],
                    "intents": record["intents"],
                    "metadata_json": record["metadata"],
                }

                if existing:
                    for key, value in values.items():
                        setattr(existing, key, value)
                    updated += 1
                else:
                    session.add(
                        KnowledgeDocument(
                            document_id=record["id"],
                            **values
                        )
                    )
                    inserted += 1

        session.commit()
        print("Ingestion successful!")
        print("Inserted:", inserted)
        print("Updated:", updated)

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    ingest()
