import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from sqlalchemy import text
from app.db.database import engine

with engine.connect() as connection:
    extensions = connection.execute(
        text("""
            SELECT name, default_version
            FROM pg_available_extensions
            WHERE name = 'vector'
        """)
    ).fetchall()

    tables = connection.execute(
        text("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)
    ).fetchall()

    print("Available vector extension:", extensions)
    print("Current database tables:", tables)