# citation_extractor.py
from email.mime import text
import re
import json
from pathlib import Path

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR  = Path(__file__).parent
JUDGMENT_TEXT  = INGESTION_DIR / "judgment_text.txt"
CITATIONS_OUT  = INGESTION_DIR / "citations.json"

# ── Extract ───────────────────────────────────────────────
def extract_citations():
    with open(JUDGMENT_TEXT, "r", encoding="utf-8") as f:
        text = f.read()

# ── Extract sections + articles ────────────────────────
    section_matches = re.findall(r"Sections?\s+([0-9(),\sand]+)", text)

    sections = set()
    for match in section_matches:
     for num in re.findall(r"\d+(?:\(\d+\))?", match):
        sections.add(f"Section {num}")

    articles = re.findall(r"Article\s+\d+", text)

    data = {
      "sections": sorted(sections),
      "articles": sorted(set(articles))
}

# ── Save ───────────────────────────────────────────────
    with open(CITATIONS_OUT, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=4)

    print(json.dumps(data, indent=4))
    print(f"Saved → {CITATIONS_OUT}")
    return data
if __name__ == "__main__":
    extract_citations()