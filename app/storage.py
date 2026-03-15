import json
from pathlib import Path

INDEX_PATH = Path("data/index.json")

def load_index() -> dict:
    if not INDEX_PATH.exists():
        return { "documents": [] }
    
    with INDEX_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
    

def save_index(data: dict) -> None:
    INDEX_PATH.parent.mkdir(exist_ok=True)

    with INDEX_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    print(f"[storage] Index saved to {INDEX_PATH}")


def save_chunks(file_path: str, chunks: list[dict]) -> None:
    INDEX_PATH.parent.mkdir(exist_ok=True)

    data = load_index()

    document_record = {
        "source": file_path,
        "chunks": chunks
    }

    existing_index = next(
       (i for i, doc in enumerate(data["documents"]) if doc["source"] == file_path),
       None,
    )

    if existing_index is not None:
        data["documents"][existing_index] = document_record
        print(f"[storage] Updated existing document: {file_path}")
    else:
        data["documents"].append(document_record)
        print(f"[storage] Added new document: {file_path}")
    
    save_index(data)


def get_documents() -> list[dict]:
    data = load_index()
    return data.get("documents", [])