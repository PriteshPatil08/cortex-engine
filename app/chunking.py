def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120)-> list[str]:
    """
    Split text into overlapping chunks.

    chunk_size: size of each chunk (in characters)
    overlap: number of characters shared between consecutive chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    
    chunks: list[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk);
        if end == n:
            break;
        start = end - overlap
        
    return chunks