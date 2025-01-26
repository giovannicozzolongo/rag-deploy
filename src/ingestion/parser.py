"""PDF and document parsing using PyMuPDF with unstructured fallback."""

import logging
from pathlib import Path

import fitz

logger = logging.getLogger(__name__)


def parse_pdf(path: str | Path) -> list[dict]:
    """Extract text from PDF, one entry per page.

    Falls back to unstructured for pages where PyMuPDF
    returns very little text (tables, multi-column layouts).
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"no such file: {path}")

    doc = fitz.open(str(path))
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text("text").strip()

        # pymupdf sometimes chokes on complex layouts
        if len(text) < 50:
            text = _parse_page_unstructured(path, i)

        if text:
            pages.append(
                {
                    "text": text,
                    "source": path.name,
                    "page": i + 1,
                }
            )

    doc.close()
    logger.info(f"parsed {len(pages)} pages from {path.name}")
    return pages


def _parse_page_unstructured(path: Path, page_num: int) -> str:
    """Fallback parser for tricky pages."""
    try:
        from unstructured.partition.pdf import partition_pdf

        elements = partition_pdf(
            str(path),
            strategy="fast",
            include_page_breaks=False,
        )
        # filter to just this page
        page_elements = [
            el
            for el in elements
            if hasattr(el, "metadata")
            and getattr(el.metadata, "page_number", None) == page_num + 1
        ]
        return "\n".join(str(el) for el in page_elements).strip()
    except Exception as e:
        logger.warning(f"unstructured fallback failed page {page_num}: {e}")
        return ""


def parse_directory(dir_path: str | Path) -> list[dict]:
    """Parse all PDFs in a directory."""
    dir_path = Path(dir_path)
    all_pages = []
    pdf_files = sorted(dir_path.glob("*.pdf"))

    if not pdf_files:
        logger.warning(f"no PDFs found in {dir_path}")
        return all_pages

    for pdf in pdf_files:
        try:
            pages = parse_pdf(pdf)
            all_pages.extend(pages)
        except Exception as e:
            logger.error(f"failed to parse {pdf.name}: {e}")

    logger.info(f"total: {len(all_pages)} pages from {len(pdf_files)} files")
    return all_pages
