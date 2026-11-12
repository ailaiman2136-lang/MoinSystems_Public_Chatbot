
import sys
import json
import math
from pathlib import Path
from sqlalchemy import select

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.db.database import SessionLocal
from app.models.knowledge import KnowledgeDocument
from app.services.embedding_service import generate_query_embeddings
from app.services.retrieval_service import get_intent_boost

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if not norm_a or not norm_b:
        return 0.0

    return dot / (norm_a * norm_b)


def main():
    evaluation_path = BASE_DIR / "data" / "evaluation_questions.jsonl"

    with open(evaluation_path, encoding="utf-8") as file:
        questions = [json.loads(line) for line in file if line.strip()]

    session = SessionLocal()

    try:
        documents = session.scalars(
            select(KnowledgeDocument).where(
                KnowledgeDocument.embedding.is_not(None)
            )
        ).all()

        queries = [item["query"].strip() for item in questions]
        query_vectors = generate_query_embeddings(queries)

        hit_at_3 = 0
        hit_at_5 = 0
        reciprocal_ranks = []

        print(f"\nEvaluation questions: {len(questions)}")
        print(f"Knowledge records: {len(documents)}")

        for question, query_vector in zip(questions, query_vectors):
            expected = question["expected_record"]

            ranked = []
            for doc in documents:
                from app.services.retrieval_service import get_intent_boost

                score = cosine_similarity(query_vector, doc.embedding)
                score += get_intent_boost(question["query"], doc.intents)
                ranked.append((doc.document_id, doc.title, score))

            ranked.sort(key=lambda item: item[2], reverse=True)

            expected_rank = next(
                (
                    rank
                    for rank, item in enumerate(ranked, start=1)
                    if item[0] == expected
                ),
                None
            )

            if expected_rank is not None:
                reciprocal_ranks.append(1 / expected_rank)

            if expected_rank is not None and expected_rank <= 3:
                hit_at_3 += 1

            if expected_rank is not None and expected_rank <= 5:
                hit_at_5 += 1

            print(f"\n{question['id']}: {question['query']}")
            print(f"Expected record: {expected}")
            print(f"Expected rank: {expected_rank or 'NOT FOUND'}")

            for record_id, title, score in ranked[:3]:
                print(f"  {record_id} | {score:.4f} | {title}")

        total = len(questions)

        print("\n========== EVALUATION SUMMARY ==========")
        print(f"Total questions: {total}")
        print(f"Hit@3: {hit_at_3}/{total} ({hit_at_3 / total:.2%})")
        print(f"Hit@5: {hit_at_5}/{total} ({hit_at_5 / total:.2%})")
        print(
            f"Mean Reciprocal Rank: "
            f"{sum(reciprocal_ranks) / total:.4f}"
        )

    finally:
        session.close()


if __name__ == "__main__":
    main()
