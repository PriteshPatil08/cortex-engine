import argparse
from pathlib import Path
from app.chunking import chunk_text

def cmd_ingest(args: argparse.Namespace) -> None:
    file_path = Path(args.path)
    
    if not file_path.exists():
        print(f"[ingest] File not found: {file_path}")
        return
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"[ingest] successfully loaded file: {file_path}")
        print(f"[ingest] Characters loaded: {len(content)}")
        print("[ingest] Preview:")
        print(content[:200])
        chunk_text(content, 800, 120)


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