
# MoinSystems AI Public Chatbot

An AI-powered public website chatbot developed using FastAPI, PostgreSQL, Gemini API and Retrieval-Augmented Generation (RAG).

## Features

- AI-powered question answering using Gemini.
- RAG-based retrieval from an approved company knowledge base.
- Semantic search using Gemini embeddings.
- Conversation history and session management.
- Lead collection and PostgreSQL storage.
- Email notifications through SMTP.
- Responsive chatbot frontend.
- API documentation through Swagger UI.

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Google Gemini API
- Gemini Embeddings
- HTML, CSS and JavaScript
- SMTP / Gmail

## Project Structure

- `app/api/` – Chat and lead APIs
- `app/db/` – Database configuration
- `app/models/` – Database models
- `app/services/` – Chat, embedding, retrieval and email services
- `frontend/` – Chatbot interface
- `data/` – Prepared knowledge and evaluation datasets
- `scripts/` – Data preparation, ingestion and evaluation scripts
- `migrations/` – Database migrations

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   pip install -r requirements.txt

3. Configure environment variables in `.env` using `.env.example`.
4. Create the PostgreSQL database.
5. Apply migrations:

   python -m alembic upgrade head

6. Prepare and ingest the approved knowledge dataset.
7. Generate embeddings.
8. Start the application:

   python -m uvicorn app.main:app --reload

## Access

- Chatbot: http://127.0.0.1:8000/
- API documentation: http://127.0.0.1:8000/docs
- Health check: /api/v1/health
- Database health: /api/v1/health/database

## Main API Endpoints

- POST `/api/v1/chat`
- POST `/api/v1/leads`
- GET `/api/v1/health`
- GET `/api/v1/health/database`

## Testing

The application was tested for:
- Backend compilation and database migrations.
- Chat API responses and conversation sessions.
- Semantic retrieval and evaluation.
- Lead submission and database storage.
- Email notification delivery.
- Frontend and backend integration.

## Security Notes

- API keys and SMTP credentials must remain in `.env`.
- Never commit `.env` or private company data.
- Use approved and verified company knowledge sources.

## Project Status

The application has been deployed on Railway and the core functionality has been verified.

- Live chatbot responses: Working
- Knowledge base: 97 records loaded
- Embeddings: 97/97 verified (768 dimensions)
- Retrieval evaluation: 96.88% Hit@5
- Lead capture and database storage: Working
- Hosted email notifications: Pending due to outbound SMTP network restrictions on Railway. Local email delivery was tested successfully.
