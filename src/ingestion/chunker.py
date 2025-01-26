"""Three chunking strategies for splitting parsed documents."""

import logging
import re

logger = logging.getLogger(__name__)


def chunk_fixed(
    pages: list[dict],
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[dict]:
    """Fixed-size character chunking with overlap."""
    chunks = []
    for page in pages:
        text = page["text"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            if chunk_text.strip():
                chunks.append(
                    {
                        "text": chunk_text.strip(),
                        "source": page["source"],
                        "page": page["page"],
                        "strategy": "fixed",
                    }
                )
            start += chunk_size - overlap
    return chunks


def chunk_recursive(
    pages: list[dict],
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[dict]:
    """Recursive text splitting — tries to split on paragraphs,
    then sentences, then characters."""
    separators = ["\n\n", "\n", ". ", " "]
    chunks = []

    for page in pages:
        text = page["text"]
        splits = _recursive_split(text, separators, chunk_size)

        # merge small splits with overlap
        merged = _merge_splits(splits, chunk_size, overlap)
        for chunk_text in merged:
            if chunk_text.strip():
                chunks.append(
                    {
                        "text": chunk_text.strip(),
                        "source": page["source"],
                        "page": page["page"],
                        "strategy": "recursive",
                    }
                )
    return chunks


def _recursive_split(
    text: str,
    separators: list[str],
    chunk_size: int,
) -> list[str]:
    if not text or len(text) <= chunk_size:
        return [text] if text else []

    sep = separators[0] if separators else ""
    remaining_seps = separators[1:] if len(separators) > 1 else []

    if sep:
        parts = text.split(sep)
    else:
        # last resort: character split
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    result = []
    current = ""
    for part in parts:
        candidate = current + sep + part if current else part
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                result.append(current)
            if len(part) > chunk_size and remaining_seps:
                result.extend(_recursive_split(part, remaining_seps, chunk_size))
            else:
                current = part
    if current:
        result.append(current)

    return result


def _merge_splits(splits: list[str], chunk_size: int, overlap: int) -> list[str]:
    """Merge small splits and add overlap between chunks."""
    merged = []
    current = ""

    for s in splits:
        if not s.strip():
            continue
        if current and len(current) + len(s) + 1 > chunk_size:
            merged.append(current)
            # keep tail for overlap
            if overlap > 0:
                current = current[-overlap:] + " " + s
            else:
                current = s
        else:
            current = current + " " + s if current else s

    if current.strip():
        merged.append(current)
    return merged


def chunk_semantic(
    pages: list[dict],
    max_chunk_size: int = 800,
) -> list[dict]:
    """Semantic chunking — split on paragraph boundaries,
    keep logical sections together."""
    chunks = []

    for page in pages:
        text = page["text"]
        paragraphs = re.split(r"\n{2,}", text)
        current = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current) + len(para) + 2 <= max_chunk_size:
                current = current + "\n\n" + para if current else para
            else:
                if current:
                    chunks.append(
                        {
                            "text": current,
                            "source": page["source"],
                            "page": page["page"],
                            "strategy": "semantic",
                        }
                    )
                # if single paragraph is too long, just keep it
                current = para

        if current.strip():
            chunks.append(
                {
                    "text": current,
                    "source": page["source"],
                    "page": page["page"],
                    "strategy": "semantic",
                }
            )

    return chunks


STRATEGIES = {
    "fixed": chunk_fixed,
    "recursive": chunk_recursive,
    "semantic": chunk_semantic,
}
