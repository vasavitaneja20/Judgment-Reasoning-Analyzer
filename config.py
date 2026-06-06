# config.py
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"

# Inputs
PDF_PATH = DATA_DIR / "judgment.pdf"

# Intermediate artifacts
JUDGMENT_TEXT = DATA_DIR / "judgment_text.txt"
PARAGRAPH_STORE = DATA_DIR / "paragraph_store.json"
STRUCTURED_JUDGMENT = DATA_DIR / "structured_judgment.json"
EMBEDDINGS_PATH = DATA_DIR / "embeddings.pkl"

# Outputs
JUDGMENT_ANALYSIS = DATA_DIR / "judgment_analysis.json"

# Models
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-2.5-flash"