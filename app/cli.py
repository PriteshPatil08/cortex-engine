import argparse
from pathlib import Path
from app.chunking import chunk_text
from app.storage import save_chunks

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
    #Placeholder: Later we'll retrieve chunks + call an LLM.
    print(f"[ask] Question: {args.question}")
    print("[ask] (Soon: answers. Today: dramatic pause...)")
    print("[ask] Answer: 42 (placeholder, but emotionally accurate).")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cortext-engine",
        description="AI-powered cortex engine (in progress)."
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest", help="Ingest a document into the knowledge base")
    ingest.add_argument("path", help="Path to a document (txt/pdf later)")
    ingest.set_defaults(func=cmd_ingest)

    return parser

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)