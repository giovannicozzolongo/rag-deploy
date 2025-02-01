"""API route handlers."""

import logging
import time

from fastapi import APIRouter, HTTPException

from src.api.models import ChunkResult, HealthResponse, QueryRequest, QueryResponse
from src.generation.generator import check_ollama, generate
from src.generation.prompt import format_prompt
from src.retrieval.retriever import retrieve

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    t0 = time.time()

    try:
        chunks = retrieve(req.question, top_k=req.top_k)
    except FileNotFoundError:
        raise HTTPException(503, "index not built — run make ingest first")

    if not chunks:
        raise HTTPException(404, "no relevant documents found")

    prompt = format_prompt(req.question, chunks)
    gen = generate(prompt)

    sources = [
        ChunkResult(
            text=c["text"][:300],
            source=c["source"],
            page=c["page"],
            score=c["score"],
        )
        for c in chunks
    ]

    return QueryResponse(
        answer=gen["answer"],
        sources=sources,
        latency_s=round(time.time() - t0, 2),
        model=gen["model"],
    )


@router.get("/health", response_model=HealthResponse)
async def health():
    index_ok = True
    try:
        from src.retrieval.vector_store import load_index

        load_index()
    except Exception:
        index_ok = False

    return HealthResponse(
        status="ok" if index_ok else "degraded",
        index_loaded=index_ok,
        ollama_available=check_ollama(),
    )
