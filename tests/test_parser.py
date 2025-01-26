"""Test PDF parsing."""

import pytest

from src.ingestion.parser import parse_pdf


def test_parse_nonexistent_raises():
    with pytest.raises(FileNotFoundError):
        parse_pdf("/tmp/nonexistent_file_12345.pdf")


def test_parse_sample_doc():
    """Check that we can parse one of our generated sample docs."""
    from pathlib import Path

    sample = Path("data/sample_docs/python_collections.pdf")
    if not sample.exists():
        pytest.skip("sample docs not generated yet")

    pages = parse_pdf(sample)
    assert len(pages) > 0
    assert all("text" in p and "source" in p for p in pages)
    # should contain something about collections
    all_text = " ".join(p["text"] for p in pages).lower()
    assert "namedtuple" in all_text or "counter" in all_text
