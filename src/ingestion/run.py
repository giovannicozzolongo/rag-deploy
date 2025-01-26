"""Run the full ingestion pipeline: parse → chunk → embed → index."""

import logging
import sys
from pathlib import Path

from src.ingestion.chunker import STRATEGIES
from src.ingestion.embedder import embed_texts
from src.ingestion.parser import parse_directory
from src.retrieval.vector_store import build_index, save_index

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

DOCS_DIR = Path("data/sample_docs")
STRATEGY = "recursive"  # best results after comparison
CHUNK_SIZE = 500
OVERLAP = 50


def main():
    logger.info("starting ingestion pipeline")

    # parse
    pages = parse_directory(DOCS_DIR)
    if not pages:
        logger.error("no pages parsed, check your docs directory")
        sys.exit(1)
    logger.info(f"parsed {len(pages)} pages total")

    # chunk
    chunk_fn = STRATEGIES[STRATEGY]
    if STRATEGY == "semantic":
        chunks = chunk_fn(pages, max_chunk_size=CHUNK_SIZE)
    else:
        chunks = chunk_fn(pages, chunk_size=CHUNK_SIZE, overlap=OVERLAP)
    logger.info(f"created {len(chunks)} chunks (strategy={STRATEGY})")

    # embed
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)
    logger.info(f"embeddings shape: {embeddings.shape}")

    # index
    index = build_index(embeddings)
    save_index(index, chunks)

    logger.info("done")


if __name__ == "__main__":
    main()
