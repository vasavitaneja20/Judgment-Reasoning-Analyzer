# embedding_builder.py
import json
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer

# ── Paths ──────────────────────────────────────────────
BASE_DIR        = Path(__file__).parent.parent
INGESTION_DIR   = BASE_DIR / "ingestion"
DATA_DIR        = BASE_DIR / "data"

PARAGRAPH_STORE = INGESTION_DIR / "paragraph_store.json"
EMBEDDINGS_PATH = DATA_DIR / "embeddings.pkl"

# ── Build ──────────────────────────────────────────────
def build_embeddings():
    with open(PARAGRAPH_STORE, "r", encoding="utf-8") as f:
        paragraphs = json.load(f)

    model  = SentenceTransformer("all-MiniLM-L6-v2")
    texts  = [p["text"] for p in paragraphs]

    embeddings = model.encode(texts, show_progress_bar=True)

    DATA_DIR.mkdir(exist_ok=True)

    with open(EMBEDDINGS_PATH, "wb") as f:
        pickle.dump(embeddings, f)

    print(f"Saved {len(embeddings)} embeddings → {EMBEDDINGS_PATH}")

if __name__ == "__main__":
    build_embeddings()