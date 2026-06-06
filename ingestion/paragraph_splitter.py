import json
import re
from pathlib import Path

# ── Paths ──────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent  # project root
INGESTION_DIR = Path(__file__).parent  # ingestion/

STRUCTURED_JUDGMENT = INGESTION_DIR / "structured_judgment.json"
PARAGRAPH_STORE = INGESTION_DIR / "paragraphs.json"


# ── Extract ───────────────────────────────────────────────
def split_paragraphs():
    with open(STRUCTURED_JUDGMENT, "r", encoding="utf-8") as f:
        data = json.load(f)

    analysis_text = data["analysis"]


# ── Clean text ─────────────────────────────────────────
    analysis_text = re.sub(r"[\x08\x0c]", " ", analysis_text)
    analysis_text = re.sub(r"\[\d{4}\]\s+\d+\s+S\.C\.R\.", "", analysis_text)
    analysis_text = re.sub(r"\n\s*\d+\s*\n", "\n", analysis_text)
    analysis_text = re.sub(r"[ \t]+", " ", analysis_text)
    analysis_text = re.sub(r"(?<!\n)\n(?!\n)", " ", analysis_text)
    analysis_text = re.sub(r"(\d+\.)", r"\n\1", analysis_text)

# ── Split into paragraphs ──────────────────────────────
    paragraphs = re.split(r"\n\s*\d+\.\s*", analysis_text)
    paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 50]

    paragraph_data = [
    {"id": i, "text": paragraph} for i, paragraph in enumerate(paragraphs)
]

# ── Save ───────────────────────────────────────────────
    with open(PARAGRAPH_STORE, "w", encoding="utf-8") as f:
       json.dump(paragraph_data, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(paragraph_data)} paragraphs → {PARAGRAPH_STORE}")
    return paragraph_data

if __name__ == "__main__":
    split_paragraphs()
