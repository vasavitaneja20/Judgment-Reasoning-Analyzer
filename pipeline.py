# pipeline.py
from pathlib import Path
import sys

# ── Ensure project root is on path ─────────────────────
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

# ── Paths ──────────────────────────────────────────────
INGESTION_DIR       = BASE_DIR / "ingestion"
DATA_DIR            = BASE_DIR / "data"
PDF_PATH            = DATA_DIR / "judgment.pdf"

DATA_DIR.mkdir(exist_ok=True)

# ── Pipeline ───────────────────────────────────────────
def run_pipeline(pdf_path: str = None):
    input_pdf = Path(pdf_path) if pdf_path else PDF_PATH

    # ── Stage 1: PDF → text ────────────────────────────
    print("[1/6] Extracting text from PDF...")
    from ingestion.pdf_extractor import extract_text
    extract_text(input_pdf)                        # takes pdf_path only, writes to INGESTION_DIR/judgment_text.txt

    # ── Stage 2: Detect sections ───────────────────────
    print("[2/6] Detecting sections...")
    from ingestion.section_detector import detect_sections
    detect_sections()                              # reads judgment_text.txt, prints found/not found

    # ── Stage 3: Split + store paragraphs ──────────────
    print("[3/6] Splitting paragraphs...")
    from ingestion.paragraph_splitter import split_paragraphs
    from ingestion.paragraph_store import store_paragraphs
    split_paragraphs()                             # writes paragraphs.json
    store_paragraphs()                             # writes paragraph_store.json

    # ── Stage 4: Extract legal entities ───────────────
    print("[4/6] Extracting legal entities...")
    from ingestion.metadata_extractor import extract_metadata
    from ingestion.citation_extractor import extract_citations
    from ingestion.precedent_extractor import extract_precedents
    from ingestion.reasoning_extractor import main as extract_reasoning
    extract_metadata()
    extract_citations()
    extract_precedents()
    extract_reasoning()

    # ── Stage 5: Build embeddings ──────────────────────
    print("[5/6] Building embeddings...")
    from analysis.embedding_builder import build_embeddings
    build_embeddings()

    # ── Stage 6: AI analysis ───────────────────────────
    print("[6/6] Running AI analysis...")
    from analysis.ai_analyzer import main as analyze
    analyze()

    print("\n✓ Pipeline complete.")
    print("Query with: python -m retrieval.rag_query_engine")

if __name__ == "__main__":
    run_pipeline()