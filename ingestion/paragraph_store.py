import json
import re
from pathlib import Path

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR   = Path(__file__).parent          # ingestion/

STRUCTURED_JUDGMENT = INGESTION_DIR / "structured_judgment.json"
PARAGRAPH_STORE     = INGESTION_DIR / "paragraph_store.json"

# ── Extract───────────────────────────────────────────────
def store_paragraphs():
     with open(STRUCTURED_JUDGMENT, "r", encoding="utf-8") as f:
         data = json.load(f)
     
     sections = [
    ("facts",       data["facts"]),
    ("submissions", data["submissions"]),
    ("analysis",    data["analysis"]),
    ("conclusion",  data["conclusion"])
]



# ── Extract paragraphs ─────────────────────────────────
     paragraph_store = []

     for section_name, text in sections:

         pattern = re.finditer(
            r"(?m)^\s*(\d+)\.\s*(.+?)(?=\n\s*\d+\.|\Z)",
            text,
            re.DOTALL
    )

         for match in pattern:

            para_no   = int(match.group(1))
            para_text = match.group(2).strip()

            if len(para_text.split()) < 20:
              continue

            paragraph_store.append({
            "id":      para_no,
            "section": section_name,
            "text":    para_text
        })

# ── Save ───────────────────────────────────────────────
     with open(PARAGRAPH_STORE, "w", encoding="utf-8") as f:
       json.dump(paragraph_store, f, indent=4)

     print(f"Saved {len(paragraph_store)} paragraphs → {PARAGRAPH_STORE}")
     return paragraph_store
if __name__ == "__main__":
    store_paragraphs()