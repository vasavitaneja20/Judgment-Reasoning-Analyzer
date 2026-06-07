# precedent_extractor.py
import json
import re
from pathlib import Path

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR  = Path(__file__).parent
JUDGMENT_TEXT  = INGESTION_DIR / "judgment_text.txt"
METADATA_PATH  = INGESTION_DIR / "metadata.json"
PRECEDENTS_OUT = INGESTION_DIR / "precedents.json"

def extract_precedents():
    with open(JUDGMENT_TEXT, "r", encoding="utf-8") as f:
        text = f.read()

    # DEBUG — find what headings actually exist
    for line in text.split("\n"):
        if "case" in line.lower() or "cited" in line.lower() or "law" in line.lower():
            print(repr(line))

# ── Extract ───────────────────────────────────────────────
def extract_precedents():
    with open(JUDGMENT_TEXT, "r", encoding="utf-8") as f:
        text = f.read()

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    current_case = metadata.get("case_name", "")

    # ── Slice section ──────────────────────────────────
    start = text.find("Case Law Cited")
    end   = text.find("Books and Periodicals Cited")
    case_law_section = text[start:end if end != -1 else start + 5000]

    # ── Flatten ALL line breaks, clean whitespace ──────
    flat = case_law_section.replace("\n", " ").replace("\xa0", " ")
    flat = re.sub(r"\s+", " ", flat).strip()

    # ── Split into individual citation entries ─────────
    # entries are separated by ; or by – held/referred
    entries = re.split(r";|–\s*(?:held|referred|overruled|followed|approved)", flat)

    # ── Extract case name from each entry ─────────────
    cases = []
    for entry in entries:
        entry = entry.strip()
        # match: Word(s) v. Word(s) — stop before citation bracket or paren
        m = re.search(
            r"([A-Z][A-Za-z.,'&()\s]+?\bv\.\s*[A-Z][A-Za-z.,'&()\s]+?)(?=\[|\(\d{4}\)|$)",
            entry
        )
        if m:
            name = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(",").strip()
            if len(name) > 5 and "v." in name:
                cases.append(name)

    # ── Deduplicate + filter current case ─────────────
    unique   = sorted(set(cases))
    filtered = [
        c for c in unique
        if current_case not in c and c not in current_case
    ]

    data = {"extracted_citations": filtered}

    with open(PRECEDENTS_OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Extracted {len(filtered)} precedents → {PRECEDENTS_OUT}")
    return data

if __name__ == "__main__":
   extract_precedents()