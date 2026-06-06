# section_detector.py
import re
from pathlib import Path

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR = Path(__file__).parent
JUDGMENT_TEXT = INGESTION_DIR / "judgment_text.txt"

SECTION_HEADINGS = [
    "FACTUAL BACKGROUND",
    "SUBMISSIONS OF THE PARTIES",
    "ANALYSIS",
    "CONCLUSION"
]

# ── Detect ─────────────────────────────────────────────
def detect_sections():
    with open(JUDGMENT_TEXT, "r", encoding="utf-8") as f:
        text = f.read()

    found = []
    for section in SECTION_HEADINGS:
        if section in text:
            print(f"Found: {section}")
            found.append(section)
        else:
            print(f"Not Found: {section}")

    return found

if __name__ == "__main__":
    detect_sections()