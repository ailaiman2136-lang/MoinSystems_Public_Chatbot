from fastapi import FastAPI
from app.db.database import check_database_connection

app = FastAPI(
    title="MoinSystems Public Chatbot",
    version="1.0.0"
)

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/health/database")
def database_health():
    check_database_connection()
    return {"database": "connected"}