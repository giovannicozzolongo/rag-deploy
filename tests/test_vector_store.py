"""Test FAISS index operations."""

import json
import tempfile
from pathlib import Path

import faiss
import numpy as np
import pytest

from src.retrieval.vector_store import build_index, load_index, save_index


@pytest.fixture
def dummy_embeddings():
    np.random.seed(42)
    return np.random.randn(10, 384).astype(np.float32)


@pytest.fixture
def dummy_chunks():
    return [
        {"text": f"chunk {i}", "source": "test.pdf", "page": 1}
        for i in range(10)
    ]


def test_build_index_shape(dummy_embeddings):
    index = build_index(dummy_embeddings)
    assert index.ntotal == 10
    assert index.d == 384


def test_save_and_load_roundtrip(dummy_embeddings, dummy_chunks):
    index = build_index(dummy_embeddings)

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        save_index(index, dummy_chunks, path=path)

        loaded_index, loaded_chunks = load_index(path=path)
        assert loaded_index.ntotal == 10
        assert len(loaded_chunks) == 10
        assert loaded_chunks[3]["text"] == "chunk 3"


def test_search_returns_correct_neighbors(dummy_embeddings):
    index = build_index(dummy_embeddings)
    # search with the first vector itself — should return itself as nearest
    query = dummy_embeddings[0:1]
    distances, indices = index.search(query, 3)
    assert indices[0][0] == 0
    assert distances[0][0] < 1e-6  # basically 0 distance


def test_load_missing_index_raises():
    with pytest.raises(FileNotFoundError):
        load_index(path=Path("/nonexistent/path"))
