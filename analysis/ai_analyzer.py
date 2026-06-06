# ai_analyzer.py
import json
import os
import re
import time
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR       = Path(__file__).parent.parent / "ingestion"
BASE_DIR            = Path(__file__).parent.parent
DATA_DIR            = BASE_DIR / "data"
CACHE_DIR           = BASE_DIR / "cache"
STRUCTURED_JUDGMENT = INGESTION_DIR / "structured_judgment.json"
ANALYSIS_OUT        = DATA_DIR / "judgment_analysis.json"

DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
cache_path = CACHE_DIR / "ai_analyzer_cache.json"

# ── Gemini setup ───────────────────────────────────────
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ── Load ───────────────────────────────────────────────
with open(STRUCTURED_JUDGMENT, "r", encoding="utf-8") as f:
    judgment = json.load(f)

facts       = judgment["facts"]
submissions = judgment["submissions"]
analysis    = judgment["analysis"]
conclusion  = judgment["conclusion"]

# ── Prompt ─────────────────────────────────────────────
prompt = f"""
You are an expert legal analyst.

Analyze the following Supreme Court judgment.

FACTS:
{facts}

SUBMISSIONS:
{submissions}

ANALYSIS:
{analysis}

CONCLUSION:
{conclusion}

Return ONLY valid JSON. No conversational text, no markdown.

Format:
{{
  "legal_issues": [],
  "court_reasoning": [],
  "holding": "",
  "legal_principles": [],
  "plain_english_summary": ""
}}
"""

# ── Helpers ────────────────────────────────────────────
def _call_model_with_backoff(prompt_text, max_retries=5):
    delay = 1
    for attempt in range(1, max_retries + 1):
        try:
            return model.generate_content(prompt_text).text
        except Exception:
            if attempt == max_retries:
                raise
            time.sleep(delay)
            delay *= 2

def _clean_response_text(text: str) -> str:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    cleaned = re.sub(r"```json\s*", "", cleaned, flags=re.IGNORECASE)
    return re.sub(r"```", "", cleaned).strip()

# ── Main ───────────────────────────────────────────────
def main():
    if cache_path.exists():
        result = cache_path.read_text(encoding="utf-8")
    else:
        result = _call_model_with_backoff(prompt)
        cache_path.write_text(result, encoding="utf-8")

    parsed_json = json.loads(_clean_response_text(result.strip()))

    with open(ANALYSIS_OUT, "w", encoding="utf-8") as f:
        json.dump(parsed_json, f, indent=4, ensure_ascii=False)

    print(f"Saved → {ANALYSIS_OUT}")

if __name__ == "__main__":
    main()