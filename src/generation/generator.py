"""LLM generation via Ollama (Mistral-7B)."""

import logging
import os
import time

import ollama as ollama_client

logger = logging.getLogger(__name__)

MODEL = "mistral"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
_client = ollama_client.Client(host=OLLAMA_HOST)


def generate(prompt: str, temperature: float = 0.1) -> dict:
    """Send prompt to Ollama and return response + timing."""
    t0 = time.time()

    response = _client.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": temperature},
    )

    elapsed = time.time() - t0
    answer = response["message"]["content"]

    logger.info(f"generated {len(answer)} chars in {elapsed:.1f}s")
    return {
        "answer": answer,
        "model": MODEL,
        "latency_s": round(elapsed, 2),
    }


def check_ollama() -> bool:
    """Quick health check — is ollama running and model loaded?"""
    try:
        models = _client.list()
        available = [m.model for m in models.models]
        if not any(MODEL in m for m in available):
            logger.warning(f"{MODEL} not found, available: {available}")
            return False
        return True
    except Exception as e:
        logger.error(f"ollama not reachable: {e}")
        return False
