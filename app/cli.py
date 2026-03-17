import argparse
from pathlib import Path

from app.chunking import chunk_text
from app.retrieval import (keyword_search, semantic_search, build_context)
from app.storage import get_documents, save_chunks
from app.embeddings import embed_text

def cmd_ingest(args: argparse.Namespace) -> None:
    file_path = Path(args.path)
    
    if not file_path.exists():
        print(f"[ingest] File not found: {file_path}")
        return
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        
        chunks = chunk_text(content, chunk_size = 800, overlap = 120)

        chunks_embeddings : list[dict] = []
        
        print(f"[ingest] Loaded : {file_path}")
        print(f"[ingest] Characters : {len(content)}")
        print(f"[ingest] Chunks created : {len(chunks)}")

        if chunks:
            print("[ingest] First chunk preview : ")
            print(chunks[0][:300])
            
            for chunk in chunks:
                embedding = embed_text(chunk, 8)
                if embedding is not None:
                    chunks_embeddings.append({"text": chunk, "embedding": embedding})

        save_chunks(args.path, chunks_embeddings)
        
    except Exception as e:
        print(f"[ingest] Error reading file: {e}")


def cmd_ask(args: argparse.Namespace) -> None:
    documents = get_documents()

    if not documents:
        print(f"[ask] No indexed documents found. Please ingest a file first.")
        return
    
    if args.mode == "keyword":
        results = keyword_search(documents = get_documents(), question = args.question, top_k = 3)
    elif args.mode == "semantic":
        results = semantic_search(documents = get_documents(), question = args.question, top_k = 3)
    else:
        raise ValueError("Invalid mode")

    if not results:
        print(f"No relevant results found.")
        return
    
    print(f"[ask] Top {len(results)} {args.mode} search matches:\n")

    context = build_context(results=results, max_chars = 1200)

    if context:
        print(f"[ask] Context Block: ")
        print("-" * 70)
        print(context)
        print("-" * 70)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cortex-engine",
        description="AI-powered cortex engine (in progress)"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest", help = "Ingest a document into the knowledge base")
    ingest.add_argument("path", help="Path to a document (txt/pdf later)")
    ingest.set_defaults(func=cmd_ingest)

    ask = subparsers.add_parser("ask", help = "Ask a question against ingested documents")
    ask.add_argument("question", help = "The question to ask")
    ask.add_argument("--mode", 
                     choices = ["keyword", "semantic"],
                     default = "keyword",
                     help = "Retrieval mode: keyword or semantic")
    
    ask.set_defaults(func=cmd_ask)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)