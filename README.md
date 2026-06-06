Legal Judgment NLP & RAG Pipeline
An end-to-end, modular Natural Language Processing (NLP) pipeline designed to ingest complex, multi-page legal judgment PDFs, extract granular structural components and metadata, and expose the processed data to an AI-powered Retrieval-Augmented Generation (RAG) query engine.

The project is cleanly split into two distinct operational units: Data Ingestion (Stage 1 to 4) and Downstream Semantic Analysis (Stage 5 & 6).

🏗️ System Architecture & Pipeline Workflow
The processing architecture follows a sequential 6-stage pipeline handled by the pipeline.py orchestrator:

[ judgment.pdf ]
       │
       ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        UNIT 1: DATA INGESTION                          │
├────────────────────────────────────────────────────────────────────────┤
│  Stage 1: PDF Extractor  ──► Generates 'judgment_text.txt'             │
│  Stage 2: Section Det.   ──► Matches core legal boundaries             │
│  Stage 3: Para Splitter  ──► Generates 'paragraphs.json' & store       │
│  Stage 4: Legal Entities ──► Extracts Metadata, Citations, Precedents, │
│                              and Judicial Reasoning                    │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     UNIT 2: DOWNSTREAM ANALYSIS                        │
├────────────────────────────────────────────────────────────────────────┤
│  Stage 5: Embedding Builder ──► Builds vector maps over paragraphs       │
│  Stage 6: AI Analyzer       ──► Executes LLM-driven analytical reports │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
                        [ RAG Query Engine Active ]


  Unit 1: Data Ingestion (Stages 1–4)
Text Conversion & Boundary Mapping: Extracts raw text from messy PDFs, handles page footers/headers, and dynamically maps out standard legal milestones (e.g., Factual Background, Submissions, Analysis, Conclusion).

Granular Indexing: Instead of treating a 90+ page document as a giant wall of text, Stage 3 isolates individual paragraphs. This preserves precise context and prevents data truncation downstream.

Legal Entity Processing: Runs specialized parallel extractors to fetch key legal properties:

Metadata: Parties, judges, jurisdiction, date.

Citations & Precedents: Previous case laws referenced within the judgment.

Reasoning: The specific semantic arguments used by the court to reach its decision.

Unit 2: Downstream Analysis & RAG (Stages 5–6)
Semantic Embeddings: Vectorizes the mapped paragraphs, allowing for contextual similarity matches instead of strict, rigid keyword matching.

AI Synthesis: Generates high-level legal abstracts, insights, and structural analysis reports using Large Language Models (LLMs).

RAG Query Engine: Exposes the end product to an active querying script (retrieval.rag_query_engine), allowing lawyers or researchers to search across the complex document with natural language questions.

🚀 Getting Started
Prerequisites
Python 3.10+

Dependencies listed in your requirements.txt (including your chosen PDF parser, embedding framework, and LLM SDK).

Installation
Clone the repository:

Bash
git clone https://github.com/yourusername/legal-judgment-nlp-pipeline.git
cd legal-judgment-nlp-pipeline
Install dependencies:

Bash
pip install -r requirements.txt
Prepare input directory and drop your target judgment PDF inside:

Bash
mkdir data
# Move your target pdf into data/judgment.pdf
Execution
To run the full end-to-end processing pipeline on the default document, simply execute:

Bash
python pipeline.py
To run it against a custom-pathed PDF document:

Python
# Pass custom path within a Python wrapper or edit the entry point execution block
run_pipeline(pdf_path="path/to/alternative_judgment.pdf")
🔍 Interaction & Querying
Once the pipeline logs ✓ Pipeline complete., your vector databases and JSON indexes are locked and ready. Interact with your data using the RAG interface:

Bash
python -m retrieval.rag_query_engine


⚖️ Advantages & Design Benefits
Context-Preserving Granularity: By splitting the document into structural sections (Facts, Submissions, Analysis, Conclusion) and then further into paragraph-level chunks, the pipeline avoids the "lost in the middle" phenomenon common in long-context LLM applications.

Domain-Specific Entity Extraction: Rather than relying on generic chunking, Stage 4 isolates distinct legal concepts (precedents, citations, and reasoning). This creates rich, multi-dimensional metadata that significantly boosts downstream RAG retrieval accuracy.

Modular, Decoupled Architecture: The system cleanly separates heavy, one-time computation (Unit 1: Data Ingestion & Embedding Construction) from real-time execution (Unit 2: Query Engine). This makes it highly scalable and easy to maintain or swap components (e.g., changing the PDF parser or the LLM provider).

Token Efficiency: Querying a targeted paragraph vector database is drastically cheaper and faster than feeding a raw 94-page legal document into an LLM for every single user question.

🛑 Technical Challenges & Mitigation Strategies
Structural Rigidity & Layout Variance: Legal judgments vary wildly across different jurisdictions and judges. Relying on strict keyword markers (like ANALYSIS) can cause the script to fail if a document uses alternative headings like COURT'S REASONING.

Mitigation: Future iterations will replace strict regex matching with a flexible, LLM-assisted semantic layout parser.

Noise and Boilerplate Handling: In long PDFs, page headers, footers, page numbers, and court watermarks often get baked right into the middle of sentences during raw text extraction, corrupting embedding quality.

Mitigation: Implemented data-cleaning regex patterns during the paragraph-splitting stage to filter out repetitive layout noise.

Sequential Processing Bottlenecks: Running multiple deep-learning-based entity extractors sequentially in Stage 4 increases the total pipeline execution time on massive documents.

Mitigation: The stage is designed with isolated functions, paving the way for transition into a concurrent pipeline using Python's asyncio or concurrent.futures.


**Credits**
Vasavi Taneja
