import argparse

def cmd_ingest(args: argparse.Namespace) -> None:
    #Placeholder: Later we'll load files, chunk text, create embeddings, store vectors.
    print(f"[ingest] Pretending to ingest: {args.path}")
    print(f"[ingest](Soon: parsing docs. Today: vibes.)")

def cmd_ask(args: argparse.Namespace) -> None:
    #Placeholder: Later we'll retrieve chunks + call an LLM.
    print(f"[ask] Question: {args.question}")
    print("[ask] (Soon: answers. Today: dramatic pause...)")
    print("[ask] Answer: 42 (placeolder, but emotionlly accurate).")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="personal-knowledge-engine",
        description="AI-powered personal knowledge engine (in progress)."
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