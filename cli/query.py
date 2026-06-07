# cli/query.py
import sys
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

import click

INGESTION_DIR = BASE_DIR / "ingestion"
DATA_DIR      = BASE_DIR / "data"

@click.command()
@click.argument("question")
@click.option("--top-k", default=5, help="Number of paragraphs to retrieve (default 5)")
@click.option("--no-ai", is_flag=True, help="Skip Gemini, show raw search results only")
def query(question, top_k, no_ai):
    """Query the analyzed judgment with a legal question."""

    import pickle
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    PARAGRAPH_STORE = INGESTION_DIR / "paragraph_store.json"
    EMBEDDINGS_PATH = DATA_DIR / "embeddings.pkl"

    # ── Build embeddings if missing ────────────────────
    if not EMBEDDINGS_PATH.exists():
        click.echo("Building embeddings for the first time...")
        from analysis.embedding_builder import build_embeddings
        build_embeddings()
        click.secho("✓ Embeddings ready\n", fg="green")

    if not PARAGRAPH_STORE.exists():
        click.secho(
            "✗ No paragraph store found. Run `judgment analyze <pdf>` first.",
            fg="red"
        )
        sys.exit(1)

    # ── Load ───────────────────────────────────────────
    with open(PARAGRAPH_STORE, "r", encoding="utf-8") as f:
        paragraphs = json.load(f)
    with open(EMBEDDINGS_PATH, "rb") as f:
        embeddings = pickle.load(f)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # ── Search ─────────────────────────────────────────
    q_emb   = model.encode([question])
    sims    = cosine_similarity(q_emb, embeddings)[0]
    indices = np.argsort(sims)[-top_k:][::-1]

    results = [
        {
            "score":   float(sims[i]),
            "id":      paragraphs[i]["id"],
            "section": paragraphs[i]["section"],
            "text":    paragraphs[i]["text"]
        }
        for i in indices
    ]

    click.echo(f"\n⚖️  Query: {question}")
    click.echo("─" * 60)

    # ── Gemini answer ──────────────────────────────────
    if not no_ai:
        import os
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                g_model = genai.GenerativeModel("gemini-2.5-flash")

                context = "\n\n".join(
                    f"PARAGRAPH ID: {r['id']}\nSECTION: {r['section']}\nTEXT:\n{r['text']}"
                    for r in results
                )
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
                resp   = g_model.generate_content(prompt)
                raw    = re.sub(r"```json|```", "", resp.text).strip()
                parsed = json.loads(raw)

                click.secho("\nANSWER", fg="cyan", bold=True)
                click.echo(parsed.get("answer", "No answer returned."))

                ids = parsed.get("supporting_paragraph_ids", [])
                if ids:
                    click.secho(f"\nSupporting paragraphs: {ids}", fg="yellow")

            except Exception as e:
                err = str(e)
                if "429" in err or "quota" in err.lower():
                    click.secho(
                        "\n⚠ Gemini quota reached. Showing raw results only.",
                        fg="yellow"
                    )
                else:
                    click.secho(f"\n⚠ Gemini error: {err}", fg="yellow")
        else:
            click.secho("\n⚠ No GEMINI_API_KEY found. Showing raw results only.", fg="yellow")

    # ── Raw results ────────────────────────────────────
    click.secho("\nRELEVANT PARAGRAPHS", fg="cyan", bold=True)
    for r in results:
        click.echo(f"\n{'─'*60}")
        click.secho(f"Para #{r['id']} · {r['section'].upper()} · Score: {r['score']:.2%}", fg="yellow")
        click.echo(r["text"][:500] + ("…" if len(r["text"]) > 500 else ""))