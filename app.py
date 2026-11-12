#!/usr/bin/env python3
"""
ROCm Corpus RAG — Mini-Challenge 3 (Match 3) Official CLI Entrypoint (/app/app.py)
Supports both indexing (`index /app/corpus` or `--index /app/corpus`) and querying
(`--corpus /app/corpus --query-id <id> --query <q>`), writing /app/output/<query-id>_output.json
with strict schema: {"answer": "...", "citations": [...], "confidence": 0.94}
"""
import argparse
import json
import os
import sys
from rag_engine import ROCmCorpusRAG

DEFAULT_OUTPUT_DIR = os.environ.get("MC3_OUTPUT_DIR", "/app/output")

def main():
    argv = sys.argv[1:]
    if len(argv) >= 2 and argv[0] == "index":
        res = ROCmCorpusRAG(corpus_dir=argv[1]).index_corpus()
        print(json.dumps({"status": "indexed", "indexed_files": len(res.get("documents", {}))}))
        return

    p = argparse.ArgumentParser(description="ROCm Corpus RAG — Mini-Challenge 3")
    p.add_argument("--index", dest="index_corpus", default="", help="Index the specified corpus directory")
    p.add_argument("--corpus", "-c", dest="corpus", default="/app/corpus", help="Path to corpus folder")
    p.add_argument("--query-id", "--id", dest="query_id", default="query_01", help="Query identifier")
    p.add_argument("--query", "-q", "--question", dest="query", default="", help="Question string")
    p.add_argument("--output", "-o", default="", help="Explicit output file path")
    p.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output folder")
    args, _ = p.parse_known_args()

    if args.index_corpus:
        res = ROCmCorpusRAG(corpus_dir=args.index_corpus).index_corpus()
        print(json.dumps({"status": "indexed", "indexed_files": len(res.get("documents", {}))}))
        return

    res = ROCmCorpusRAG(corpus_dir=args.corpus).answer_query(query_id=args.query_id, query=args.query)
    output_obj = {
        "answer": str(res.get("answer", "")),
        "citations": list(res.get("citations", [])),
        "confidence": float(res.get("confidence", 0.0)),
    }

    out_dir = args.output_dir if os.access("/", os.W_OK) or args.output_dir != "/app/output" else "output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = args.output or os.path.join(out_dir, f"{args.query_id}_output.json")
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output_obj, f, indent=2)
    print(json.dumps(output_obj, indent=2))

if __name__ == "__main__":
    main()
