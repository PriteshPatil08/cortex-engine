import hashlib

def embed_text(text: str, dimensions : int = 8) -> list[float]:
    """
    Create a deterministic fake embedding from text.

    This is only for learning the pipeline structure.
    Later we will replace it with a real embedding model/API.
    """

    digest = hashlib.sha256(text.encode("utf-8")).digest()

    vectors = []                                
    for i in range(dimensions):
        byte_value = digest[i]
        normalized = byte_value/255.0
        vectors.append(normalized)

    return vectors