"""Pydantic request/response models."""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)


class ChunkResult(BaseModel):
    text: str
    source: str
    page: int
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[ChunkResult]
    latency_s: float
    model: str


class HealthResponse(BaseModel):
    status: str
    index_loaded: bool
    ollama_available: bool
