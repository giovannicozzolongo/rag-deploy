"""FAISS vector store — build, save, load."""

import json
import logging
from pathlib import Path

import faiss
import numpy as np

logger = logging.getLogger(__name__)

INDEX_DIR = Path("data/index")


def build_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """Build a flat L2 index from embeddings.

    Flat is fine for < 100k vectors. Switch to IVF if it gets slow.
    """
    dim = embeddings.shape[1]
    # tried cosine (IndexFlatIP) first but L2 works better
    # probably because MiniLM embeddings aren't always normalized
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    logger.info(f"built index: {index.ntotal} vectors, dim={dim}")
    return index


def save_index(
    index: faiss.IndexFlatL2,
    chunks: list[dict],
    path: Path | None = None,
) -> None:
    """Persist index + chunk metadata to disk."""
    path = path or INDEX_DIR
    path.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(path / "vectors.faiss"))

    with open(path / "chunks.json", "w") as f:
        json.dump(chunks, f, ensure_ascii=False)

    logger.info(f"saved index to {path}")


def load_index(path: Path | None = None) -> tuple[faiss.IndexFlatL2, list[dict]]:
    """Load index + metadata from disk."""
    path = path or INDEX_DIR
    index_file = path / "vectors.faiss"
    chunks_file = path / "chunks.json"

    if not index_file.exists():
        raise FileNotFoundError(f"no index at {index_file}")

    index = faiss.read_index(str(index_file))
    with open(chunks_file) as f:
        chunks = json.load(f)

    logger.info(f"loaded index: {index.ntotal} vectors")
    return index, chunks
