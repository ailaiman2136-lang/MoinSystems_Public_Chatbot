from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(30), nullable=False)
    company = Column(String(150), nullable=True)
    project_details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())