"""Retrieve top-k chunks for a query."""

import logging

from src.ingestion.embedder import embed_query
from src.retrieval.vector_store import load_index

logger = logging.getLogger(__name__)

_index = None
_chunks = None


def _ensure_loaded():
    global _index, _chunks
    if _index is None:
        _index, _chunks = load_index()


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Query the index and return top_k chunks with scores."""
    _ensure_loaded()

    q_emb = embed_query(query)
    distances, indices = _index.search(q_emb, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        chunk = _chunks[idx].copy()
        chunk["score"] = float(dist)
        results.append(chunk)

    return results


def retrieve_batch(queries: list[str], top_k: int = 5) -> list[list[dict]]:
    """Batch retrieval for evaluation."""
    _ensure_loaded()

    from src.ingestion.embedder import embed_texts

    q_embs = embed_texts(queries)
    distances, indices = _index.search(q_embs, top_k)

    all_results = []
    for dists, idxs in zip(distances, indices):
        results = []
        for dist, idx in zip(dists, idxs):
            if idx == -1:
                continue
            chunk = _chunks[idx].copy()
            chunk["score"] = float(dist)
            results.append(chunk)
        all_results.append(results)

    return all_results


def reset():
    """Clear cached index (for testing)."""
    global _index, _chunks
    _index = None
    _chunks = None
