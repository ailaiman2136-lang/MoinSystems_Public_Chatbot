import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.services.retrieval_service import retrieve_documents

queries = [
    "What does MoinSystems AI do?",
    "Can you build an AI chatbot?",
    "Do you provide pricing?",
    "Do you offer mobile app development?",
    "What is the weather on Mars?"
]

for query in queries:
    print("\nQUESTION:", query)
    results = retrieve_documents(query)

    if not results:
        print("No relevant information found.")
        continue

    for result in results:
        print(
            result["id"],
            "| Score:", result["score"],
            "|", result["title"]
        )