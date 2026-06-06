# precedent_extractor.py
import json
import re
from pathlib import Path

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR  = Path(__file__).parent
JUDGMENT_TEXT  = INGESTION_DIR / "judgment_text.txt"
METADATA_PATH  = INGESTION_DIR / "metadata.json"
PRECEDENTS_OUT = INGESTION_DIR / "precedents.json"

# ── Extract ───────────────────────────────────────────────
def extract_precedents():
   with open(JUDGMENT_TEXT, "r", encoding="utf-8") as f:
     text = f.read()

   with open(METADATA_PATH, "r", encoding="utf-8") as f:
     metadata = json.load(f)

   current_case = metadata.get("case_name", "")

# ── Slice relevant section ─────────────────────────────
   start          = text.find("Case Law Cited")
   end            = text.find("Books and Periodicals Cited")
   case_law_section = text[start:end]

   print("--- Section Preview ---")
   print(case_law_section[:3000])
   print("-" * 23)

# ── Extract + clean precedents ─────────────────────────
   raw_cases    = re.findall(
    r"([A-Z][A-Za-z .&]+ v\. [A-Z][A-Za-z .,&]+)",
    case_law_section
)
   unique_cases = sorted(set(case.strip() for case in raw_cases))
   filtered_cases = [
    case for case in unique_cases
    if current_case not in case and case not in current_case
]

   data = {"extracted_citations": filtered_cases}

# ── Save ───────────────────────────────────────────────
   with open(PRECEDENTS_OUT, "w", encoding="utf-8") as f:
     json.dump(data, f, indent=4)

   print(json.dumps(data, indent=4))
   print(f"Saved → {PRECEDENTS_OUT}")
   return data

if __name__ == "__main__":
   extract_precedents()