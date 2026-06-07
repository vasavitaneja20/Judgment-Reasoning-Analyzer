# Judgment Reasoning Analyzer

A legal judgment analysis pipeline for extracting structured reasoning, citations, metadata, and embeddings from Supreme Court judgment PDFs. The project ingests a judgment PDF, converts it into text, detects sections, splits paragraphs, extracts legal entities and precedent citations, builds semantic embeddings, and enables AI-powered querying.

## Key Features

- PDF to structured text extraction
- Section detection for judgments (facts, submissions, analysis, conclusion)
- Paragraph splitting and indexing
- Extraction of metadata, cited statutes, and precedent cases
- Sentence embedding generation using `sentence-transformers`
- AI-driven legal analysis with Google Gemini
- Interactive CLI for analysis, querying, and result display

## Project Structure

- `pipeline.py` – orchestrates the full end-to-end processing pipeline
- `config.py` – central project paths, output locations, and model settings
- `cli/` – command-line interface entrypoints for analyze, query, and show
- `ingestion/` – document ingestion, extraction, paragraph storage, and citation extraction
- `analysis/` – embedding building and AI-based judgment analysis
- `retrieval/` – semantic retrieval and query engine
- `data/` – data artifacts created by the pipeline
- `cache/` – cached intermediate AI results

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd Judgement-Reasoning-Analyzer
```

2. Create and activate a Python virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Install the package entry point (optional):

```powershell
pip install -e .
```

## Requirements

- Python 3.10+ (recommended)
- `click`
- `google-generativeai`
- `sentence-transformers`
- `scikit-learn`
- `numpy`
- `pymupdf`
- `python-dotenv`

## Environment Setup

Create a `.env` file in the repository root with the following:

```text
GEMINI_API_KEY=your_google_gemini_api_key
```

## Usage

### Full Pipeline

Run the main pipeline from the repository root:

```powershell
python pipeline.py
```

This executes the end-to-end process:

1. Extract text from `data/judgment.pdf`
2. Detect judgment sections
3. Split the judgment into paragraphs and store them
4. Extract metadata, citations, precedents, and reasoning
5. Build embeddings for semantic search
6. Run AI analysis on the structured judgment

### CLI Commands

If the package is installed, use the `judgment` CLI.

#### Analyze a judgment PDF

```powershell
judgment analyze path\to\judgment.pdf
```

#### Query the analyzed judgment

```powershell
judgment query "What is the holding?"
```

Options:
- `--top-k` — number of paragraphs retrieved (default: 5)
- `--no-ai` — skip Gemini and display only raw retrieval results

#### Show structured output

```powershell
judgment show
```

Display a specific section:

```powershell
judgment show --section facts
```

## How It Works

### Ingestion

- `ingestion/pdf_extractor.py` reads the PDF and writes plain text
- `ingestion/section_detector.py` identifies judgment sections
- `ingestion/paragraph_splitter.py` splits the document into paragraphs
- `ingestion/paragraph_store.py` stores paragraphs in JSON for retrieval
- `ingestion/metadata_extractor.py` captures case details and docket metadata
- `ingestion/citation_extractor.py` extracts statutes and article citations
- `ingestion/precedent_extractor.py` identifies cited cases
- `ingestion/reasoning_extractor.py` extracts reasoning text

### Analysis

- `analysis/embedding_builder.py` creates sentence embeddings stored at `data/embeddings.pkl`
- `analysis/ai_analyzer.py` uses Google Gemini to analyze judgment structure and produce JSON output

### Retrieval

- `retrieval/rag_query_engine.py` performs semantic search over paragraph embeddings and asks Gemini to answer questions using retrieved evidence

## Outputs

Generated artifacts include:

- `data/judgment_text.txt`
- `data/embeddings.pkl`
- `ingestion/paragraph_store.json`
- `ingestion/metadata.json`
- `ingestion/citations.json`
- `ingestion/precedents.json`
- `ingestion/structured_judgment.json`
- `data/judgment_analysis.json`
- `cache/ai_analyzer_cache.json`

## Notes

- The pipeline currently expects the input PDF at `data/judgment.pdf` when run via `pipeline.py`
- The query engine requires a built paragraph store and embeddings; these are generated automatically if missing
- Gemini is optional for retrieval, but strongly recommended for clean legal question answering

## Development

- Add or update ingestion rules under `ingestion/` for new judgment formats
- Extend the AI prompt logic in `analysis/ai_analyzer.py` and `retrieval/rag_query_engine.py`
- Improve section detection and paragraph segmentation for richer structured output

## License

This repository does not include a license file; add one if you intend to reuse or distribute the code.
