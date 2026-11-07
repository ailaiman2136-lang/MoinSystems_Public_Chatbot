from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Check your .env file.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def check_database_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True