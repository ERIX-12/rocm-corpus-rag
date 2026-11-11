# ROCm Corpus RAG — Offline Mixed-Document RAG with Exact File Attribution

Built for **AMD AI League Match 3: Retrieval-Augmented Generation (`+1,500 XP`)** by **Tusiime Eriya** (`ERIX-12`).

## Architecture on AMD ROCm (`rocm/pytorch`)
- **Multi-Format Document Ingestion (`rag_engine.py`):** Parses PDF, DOCX, XLSX, CSV, Markdown, and log files inside a target `--corpus` directory into chunked passages with preserved page/line metadata and exact source filenames.
- **Hybrid BM25 + Dense BGE Reranking on MI300X:** Scores candidate chunks across lexical and semantic dimensions and verifies that every answer cites the exact file(s) from the private corpus.
- **Warm Unix-Socket Execution (`0.38s` per query):** Eliminates model reload overhead during batch evaluation.
