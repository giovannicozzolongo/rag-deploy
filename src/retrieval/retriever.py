"""Retrieve top-k chunks for a query."""

import logging
from pathlib import Path

from src.ingestion.embedder import embed_query
from src.retrieval.vector_store import load_index

logger = logging.getLogger(__name__)

_index = None
_chunks = None


def _ensure_loaded(index_path: Path | None = None):
    global _index, _chunks
    if _index is None:
        _index, _chunks = load_index(path=index_path)
        logger.info(f"loaded {_index.ntotal} vectors")


def _build_results(distances, indices) -> list[dict]:
    """Turn FAISS output into chunk dicts with scores."""
    results = []
    for dist, idx in zip(distances, indices):
        if idx == -1:
            continue
        chunk = _chunks[idx].copy()
        chunk["score"] = float(dist)
        results.append(chunk)
    return results


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Query the index and return top_k chunks with scores."""
    _ensure_loaded()

    q_emb = embed_query(query)
    distances, indices = _index.search(q_emb, top_k)
    return _build_results(distances[0], indices[0])


def retrieve_batch(queries: list[str], top_k: int = 5) -> list[list[dict]]:
    """Batch retrieval for evaluation."""
    _ensure_loaded()

    from src.ingestion.embedder import embed_texts

    q_embs = embed_texts(queries)
    distances, indices = _index.search(q_embs, top_k)
    return [_build_results(d, i) for d, i in zip(distances, indices)]


def reset():
    """Clear cached index (for testing)."""
    global _index, _chunks
    _index = None
    _chunks = None
