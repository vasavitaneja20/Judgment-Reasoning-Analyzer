# semantic_search.py
import json
import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR   = Path(__file__).parent.parent / "ingestion"
DATA_DIR        = Path(__file__).parent.parent / "data"
PARAGRAPH_STORE = INGESTION_DIR / "paragraph_store.json"
EMBEDDINGS_PATH = DATA_DIR / "embeddings.pkl"

# ── Load ───────────────────────────────────────────────
with open(PARAGRAPH_STORE, "r", encoding="utf-8") as f:
    paragraphs = json.load(f)

with open(EMBEDDINGS_PATH, "rb") as f:
    embeddings = pickle.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

# ── Search ─────────────────────────────────────────────
def search(query, top_k=5):
    query_embedding = model.encode([query])
    similarities    = cosine_similarity(query_embedding, embeddings)[0]
    top_indices     = np.argsort(similarities)[-top_k:][::-1]

    return [
        {
            "score":     float(similarities[idx]),
            "paragraph": paragraphs[idx]
        }
        for idx in top_indices
    ]

# ── Run standalone ─────────────────────────────────────
if __name__ == "__main__":
    results = search("Why did the Supreme Court cancel bail?")

    for r in results:
        print("\n" + "=" * 60)
        print("Similarity:", r["score"])
        print("Section:",    r["paragraph"]["section"])
        print(r["paragraph"]["text"][:500])