import argparse
from pathlib import Path

from app.chunking import chunk_text
from app.retrieval import find_best_chunk
from app.storage import get_documents, save_chunks

def cmd_ingest(args: argparse.Namespace) -> None:
    file_path = Path(args.path)
    
    if not file_path.exists():
        print(f"[ingest] File not found: {file_path}")
        return
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        
        chunks = chunk_text(content, chunk_size = 800, overlap = 120)
        
        print(f"[ingest] Loaded : {file_path}")
        print(f"[ingest] Characters : {len(content)}")
        print(f"[ingest] Chunks created : {len(chunks)}")

        if chunks:
            print("[ingest] First chunk preview : ")
            print(chunks[0][:300])

        save_chunks(args.path, chunks)
        
    except Exception as e:
        print(f"[ingest] Error reading file: {e}")


def cmd_ask(args: argparse.Namespace) -> None:
    documents = get_documents()

    if not documents:
        print(f"[ask] No indexed documents found. Please ingest a file first.")
        return

    source, chunk, score = find_best_chunk(documents, args.question)

    print(f"[ask] Question : {args.question}")

    if not chunk:
        print(f"No relevant result found.")
        return

    print(f"[ask] Best match score : {score}")
    print(f"[ask] Source: {source}")
    print(f"[ask] Answer preview:")
    print(chunk[:500])


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
    ask.set_defaults(func=cmd_ask)

    return parser

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)