
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.db.database import check_database_connection
from app.api.chat import router as chat_router
from app.api.leads import router as leads_router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="MoinSystems Public Chatbot",
    version="1.0.0"
)

app.include_router(chat_router, prefix="/api/v1")
app.include_router(leads_router, prefix="/api/v1")


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "frontend" / "index.html")


@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/v1/health/database")
def database_health():
    check_database_connection()
    return {"database": "connected"}
