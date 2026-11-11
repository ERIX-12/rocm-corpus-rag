#!/usr/bin/env python3
"""
ROCm Corpus RAG — AMD AI League Match 3 Entrypoint (/app/app.py)
Answers questions from a mixed-document corpus and returns exact source filenames.
"""
import argparse
import json
import os
import time
from rag_engine import ROCmCorpusRAG

def main():
    parser = argparse.ArgumentParser(description="ROCm Corpus RAG — Match 3")
    parser.add_argument("--query", "-q", "--question", dest="query", default="", help="Question to answer")
    parser.add_argument("--query-id", "--id", dest="query_id", default="rag_001", help="Unique query ID")
    parser.add_argument("--corpus", "-c", "--input-dir", dest="corpus", default="sample_docs", help="Mixed-document corpus directory")
    parser.add_argument("--output", "-o", default="", help="Output JSON file path")
    parser.add_argument("--output-dir", default="/app/output", help="Output directory")
    args = parser.parse_args()

    out_dir = args.output_dir if os.access("/", os.W_OK) else "output"
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.perf_counter()
    rag = ROCmCorpusRAG(corpus_dir=args.corpus)
    res = rag.answer_query(query_id=args.query_id, query=args.query)
    res["latency_sec"] = round(time.perf_counter() - t0, 4)

    out_path = args.output or os.path.join(out_dir, f"{args.query_id}_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
