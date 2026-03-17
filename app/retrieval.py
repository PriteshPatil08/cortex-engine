import re
from app.embeddings import embed_text
import math

def dot_product(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def vector_norm(vector: list[float]) -> float:
    return math.sqrt(sum(x * x for x in vector))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    return dot_product(a, b)/(vector_norm(a) * vector_norm(b))


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def score_chunk_by_semantic(chunk_embedding: list[float], question_embedding: list[float]) -> float:
    return cosine_similarity(chunk_embedding, question_embedding)


def score_chunk_by_keyword(chunk_text: str, question: str) -> int:
    chunk_text_tokens = tokenize(chunk_text)
    question_tokens = tokenize(question)

    return sum(chunk_text_tokens.count(token) for token in question_tokens)


def find_best_chunk(documents: list[dict], question: str) -> tuple[str | None, str | None, int]:    
    best_source = None
    best_chunk = None
    best_score = 0

    for document in documents:
        source = document["source"]
        for chunk in document["chunks"]:
            score = score_chunk_by_keyword(chunk["text"], question)
            if score > best_score:
                best_source = source
                best_chunk = chunk
                best_score = score

    return best_source, best_chunk, best_score


def keyword_search(documents: list[dict], question: str, top_k: int = 3) -> list[dict]:    
    results = []

    for document in documents:
        source = document["source"]
        for chunk in document["chunks"]:
            score = score_chunk_by_keyword(chunk["text"], question)
            if score > 0:
                results.append(
                    {
                        "source": source, 
                        "chunk": chunk["text"], 
                        "score": score
                    }
                )

    results.sort(key = lambda x : x["score"], reverse = True)

    return results[:top_k]


def semantic_search(documents : list[dict], question : str, top_k : int = 3) -> list[dict]:
    question_embedding = embed_text(question)
    results : list[dict] = []

    for document in documents:
        source = document["source"]
        for chunk in document["chunks"]:
            score = score_chunk_by_semantic(chunk["embedding"], question_embedding)
            chunk = chunk["text"]
            results.append({
                "source" : source,
                "chunk" : chunk,
                "score" : score
            })

    results.sort(key = lambda x : x["score"], reverse = True)
    return results[:top_k]


def build_context(results: list[dict], max_chars: int = 1200) -> str :
    context_parts_formatted = []
    context_chars_so_far = 0

    for result in results:
        source = result["source"]
        chunk = result["chunk"]

        formatted = f"[Source: {source}]\n{chunk}\n"

        if context_chars_so_far + len(formatted) > max_chars:
            remaining_chars = max_chars - context_chars_so_far
            context_parts_formatted.append(formatted[:remaining_chars])
            break

        context_parts_formatted.append(formatted)
        context_chars_so_far += len(formatted)

    return "\n".join(context_parts_formatted)