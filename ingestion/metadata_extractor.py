# metadata_extractor.py
from email import header
import re
import json
from pathlib import Path

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR  = Path(__file__).parent
JUDGMENT_TEXT  = INGESTION_DIR / "judgment_text.txt"
METADATA_OUT   = INGESTION_DIR / "metadata.json"

# ── Extract ───────────────────────────────────────────────
def extract_metadata():
    with open(JUDGMENT_TEXT, "r", encoding="utf-8") as f:
       text = f.read()

    header   = text[:1500]
    metadata = {}

# ── Extract fields ─────────────────────────────────────
    date_match = re.search(r"\d{1,2}\s+[A-Z][a-z]+\s+\d{4}", header)
    if date_match:
       metadata["date"] = date_match.group()

    judge_match = re.search(r"\[(.*?)JJ\.\]", header, re.DOTALL)
    if judge_match:
       judges_text = judge_match.group(1).replace("*", "")
       metadata["judges"] = [
        j.strip().rstrip(",")
        for j in judges_text.split("and")
    ]
  
    case_match = re.search(  r"\n([A-Za-z ]+)\s*\nv\.\s*\n([A-Za-z .&]+)", header
)
    if case_match:
        metadata["case_name"] = (
        f"{case_match.group(1).strip()} v. {case_match.group(2).strip()}"
      )

# ── Save ───────────────────────────────────────────────
    with open(METADATA_OUT, "w", encoding="utf-8") as f:
       json.dump(metadata, f, indent=4)

    print(json.dumps(metadata, indent=4))
    print(f"Saved → {METADATA_OUT}")
    return metadata

if __name__ == "__main__":    extract_metadata()