
import json
import re
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_FILE = BASE_DIR / "data" / "MoinSystems_AI_Public_Chatbot_RAG_Dataset_v2 (1).xlsx"
DATA_DIR = BASE_DIR / "data"

def clean_text(value):
    if pd.isna(value):
        return None
    value = str(value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()

def split_values(value):
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]

def write_jsonl(filename, records):
    path = DATA_DIR / filename
    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Created {filename}: {len(records)} records")

def main():
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {SOURCE_FILE}")

    knowledge = pd.read_excel(SOURCE_FILE, sheet_name="RAG_Knowledge")
    evaluation = pd.read_excel(SOURCE_FILE, sheet_name="RAG_Evaluation")

    required = [
        "ID", "Title", "Category", "Tags", "Intents",
        "Content", "Embedding Text", "Data Status"
    ]

    missing_columns = [col for col in required if col not in knowledge.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    if knowledge["ID"].duplicated().any():
        raise ValueError("Duplicate knowledge record IDs found.")

    approved = knowledge[
        knowledge["Data Status"] == "cleaned_validated"
    ].copy()

    excluded = knowledge[
        knowledge["Data Status"] != "cleaned_validated"
    ].copy()

    records = []

    for _, row in approved.iterrows():
        record = {
            "id": clean_text(row["ID"]),
            "title": clean_text(row["Title"]),
            "category": clean_text(row["Category"]),
            "tags": split_values(clean_text(row["Tags"])),
            "intents": split_values(clean_text(row["Intents"])),
            "content": clean_text(row["Content"]),
            "embedding_text": clean_text(row["Embedding Text"]),
            "metadata": {
                "data_status": clean_text(row["Data Status"]),
                "source_basis": clean_text(row["Source Basis"])
            }
        }

        if not all([
            record["id"], record["title"], record["category"],
            record["content"], record["embedding_text"]
        ]):
            raise ValueError(f"Required field missing in {record['id']}")

        records.append(record)

    evaluation_records = []

    for _, row in evaluation.iterrows():
        evaluation_records.append({
            "id": clean_text(row["ID"]),
            "query": clean_text(row["Query"]),
            "expected_record": clean_text(row["Expected Record"]),
            "expected_intent": clean_text(row["Expected Intent"])
        })

    excluded_records = []

    for _, row in excluded.iterrows():
        excluded_records.append({
            "id": clean_text(row["ID"]),
            "title": clean_text(row["Title"]),
            "category": clean_text(row["Category"]),
            "content": clean_text(row["Content"]),
            "data_status": clean_text(row["Data Status"]),
            "source_basis": clean_text(row["Source Basis"])
        })

    write_jsonl("knowledge_base.jsonl", records)
    write_jsonl("evaluation_questions.jsonl", evaluation_records)
    write_jsonl("excluded_source_gaps.jsonl", excluded_records)

    print("\nPreparation summary")
    print("Approved knowledge records:", len(records))
    print("Evaluation questions:", len(evaluation_records))
    print("Excluded source-gap records:", len(excluded_records))
    print("Original Excel file was not modified.")

if __name__ == "__main__":
    main()
