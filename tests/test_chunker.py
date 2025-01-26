"""Test chunking strategies."""

import pytest

from src.ingestion.chunker import chunk_fixed, chunk_recursive, chunk_semantic


@pytest.fixture
def sample_pages():
    return [
        {
            "text": "First paragraph about Python.\n\nSecond paragraph about collections. "
            "This has more content to make it longer than a typical chunk boundary. "
            "We need enough text here to actually trigger chunking behavior.\n\n"
            "Third paragraph about deques and their O(1) operations. "
            "Deques are great for queues and stacks alike.",
            "source": "test.pdf",
            "page": 1,
        }
    ]


def test_fixed_chunks_have_overlap(sample_pages):
    chunks = chunk_fixed(sample_pages, chunk_size=100, overlap=20)
    assert len(chunks) >= 2
    # with overlap, total text covered should be less than sum of chunk lengths
    total_chars = sum(len(c["text"]) for c in chunks)
    original_len = len(sample_pages[0]["text"])
    assert total_chars > original_len, "overlap means we re-cover some text"


def test_recursive_respects_max_size(sample_pages):
    chunks = chunk_recursive(sample_pages, chunk_size=150, overlap=20)
    for c in chunks:
        # some tolerance since merging can slightly exceed
        assert len(c["text"]) < 200, f"chunk too long: {len(c['text'])}"


def test_semantic_splits_on_paragraphs(sample_pages):
    chunks = chunk_semantic(sample_pages, max_chunk_size=200)
    assert len(chunks) >= 2
    # each chunk should have source metadata
    for c in chunks:
        assert c["source"] == "test.pdf"
        assert c["strategy"] == "semantic"


def test_empty_input():
    assert chunk_fixed([], chunk_size=100, overlap=10) == []
    assert chunk_recursive([], chunk_size=100, overlap=10) == []
    assert chunk_semantic([], max_chunk_size=200) == []
