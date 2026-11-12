from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(100), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(100))
    content = Column(Text, nullable=False)
    tags = Column(JSON)
    intents = Column(JSON)
    metadata_json = Column(JSON)
    embedding = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())