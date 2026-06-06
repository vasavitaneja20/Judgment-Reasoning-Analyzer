# pdf_extractor.py
import fitz
from pathlib import Path

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR = Path(__file__).parent
JUDGMENT_TEXT = INGESTION_DIR / "judgment_text.txt"

# ── Extract ────────────────────────────────────────────
def extract_text(pdf_path: Path):
    doc  = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    with open(JUDGMENT_TEXT, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Extracted {len(doc)} pages → {JUDGMENT_TEXT}")
    return text

if __name__ == "__main__":
    # default path for standalone run
    pdf_path = INGESTION_DIR.parent / "data" / "judgment.pdf"
    extract_text(pdf_path)