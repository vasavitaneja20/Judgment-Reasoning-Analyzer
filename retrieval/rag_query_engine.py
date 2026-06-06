# rag_query_engine.py
import json
import os
import pickle
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai

load_dotenv()

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR   = Path(__file__).parent.parent / "ingestion"
DATA_DIR        = Path(__file__).parent.parent / "data"
PARAGRAPH_STORE = INGESTION_DIR / "paragraph_store.json"
EMBEDDINGS_PATH = DATA_DIR / "embeddings.pkl"

# ── Gemini setup ───────────────────────────────────────
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_gemini = genai.GenerativeModel("gemini-2.5-flash")

# ── Load ───────────────────────────────────────────────
with open(PARAGRAPH_STORE, "r", encoding="utf-8") as f:
    paragraphs = json.load(f)

with open(EMBEDDINGS_PATH, "rb") as f:
    embeddings = pickle.load(f)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ── Retrieve ───────────────────────────────────────────
def retrieve(query, top_k=5):
    query_embedding = embedding_model.encode([query])
    similarities    = cosine_similarity(query_embedding, embeddings)[0]
    top_indices     = np.argsort(similarities)[-top_k:][::-1]

    return [
        {
            "score":   float(similarities[idx]),
            "id":      paragraphs[idx]["id"],
            "section": paragraphs[idx]["section"],
            "text":    paragraphs[idx]["text"]
        }
        for idx in top_indices
    ]

# ── Main ───────────────────────────────────────────────
def main():
    question = input("\nAsk a legal question: ")
    results  = retrieve(question)

    context       = ""
    supporting_ids = []

    for r in results:
        supporting_ids.append(r["id"])
        context += f"""
PARAGRAPH ID: {r['id']}
SECTION: {r['section']}
TEXT:
{r['text']}
"""

    prompt = f"""
You are a legal reasoning assistant.

Answer ONLY using the evidence provided.

QUESTION:
{question}

EVIDENCE:
{context}

Return valid JSON only.

Format:
{{
    "answer": "",
    "supporting_paragraph_ids": []
}}
"""

    response = model_gemini.generate_content(prompt)
    print("\n")
    print(response.text)

if __name__ == "__main__":
    main()