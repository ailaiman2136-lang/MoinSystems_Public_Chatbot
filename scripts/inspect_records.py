import json

ids = {
    "company_001",
    "phase2_lead_capture_001",
    "phase2_pricing_001"
}

for filename in [
    "data/knowledge_base.jsonl",
    "data/excluded_source_gaps.jsonl"
]:
    print("\nFILE:", filename)

    with open(filename, encoding="utf-8-sig") as f:
        for line in f:
            record = json.loads(line)

            if record.get("id") in ids:
                print("\nID:", record.get("id"))
                print("TITLE:", record.get("title"))
                print("CONTENT:", record.get("content"))