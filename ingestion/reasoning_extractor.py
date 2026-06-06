# reasoning_extractor.py
import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR      = Path(__file__).parent
BASE_DIR           = INGESTION_DIR.parent
CACHE_DIR          = BASE_DIR / "cache"
STRUCTURED_JUDGMENT = INGESTION_DIR / "structured_judgment.json"
REASONING_OUT      = INGESTION_DIR / "reasoning.json"

CACHE_DIR.mkdir(exist_ok=True)
cache_path = CACHE_DIR / "reasoning_extractor_cache.json"

# ── Gemini setup ───────────────────────────────────────
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ── Load ───────────────────────────────────────────────
with open(STRUCTURED_JUDGMENT, "r", encoding="utf-8") as f:
    judgment = json.load(f)

analysis   = judgment["analysis"][:15000]
conclusion = judgment["conclusion"][:5000]

# ── Prompt ─────────────────────────────────────────────
prompt = f"""
You are a senior legal researcher.

Analyze the ANALYSIS section and CONCLUSION section
of a Supreme Court judgment.

ANALYSIS:
{analysis}

CONCLUSION:
{conclusion}

Extract:
1. Legal Principles relied upon by the Court.
2. Major Findings reached by the Court.
3. Reasoning Chains (Premise → Legal Rule → Application → Conclusion).
4. Explain how the Court's reasoning led to the final holding.

Return ONLY valid JSON.

Format:
{{
  "legal_principles": [{{"principle": ""}}],
  "major_findings":   [{{"finding": ""}}],
  "reasoning_chains": [{{
      "premise": "",
      "legal_rule": "",
      "application": "",
      "conclusion": ""
  }}],
  "reasoning_to_holding": ""
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

# ── Main ───────────────────────────────────────────────
def main():
    if cache_path.exists():
        result = cache_path.read_text(encoding="utf-8")
    else:
        try:
            result = _call_model_with_backoff(prompt)
            cache_path.write_text(result, encoding="utf-8")
        except Exception as e:
            print(f"Gemini error: {e}")
            return

    print(result)

if __name__ == "__main__":
    main()