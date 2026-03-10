import re

def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())

def score_chunk(chunk: str, query_terms: list[str]) -> int:
    chunk_terms = tokenize(chunk)
    return sum(chunk_terms.count(term) for term in query_terms)

def find_best_chunk(documents: list[dict], question: str) -> tuple[str | None, str | None, int]:
    query_terms = tokenize(question)

    best_source = None
    best_chunk = None
    best_score = 0

    for document in documents:
        source = document["source"]
        for chunk in document["chunks"]:
            score = score_chunk(chunk, query_terms)
            if score > best_score:
                best_source = source
                best_chun = chunk
                best_score = score

    return best_source, best_chunk, best_score