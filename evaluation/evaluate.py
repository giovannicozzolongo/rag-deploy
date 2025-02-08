"""Evaluate retrieval and generation quality on test set."""

import json
import logging
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

QUESTIONS_PATH = Path("evaluation/test_questions.json")


def load_questions() -> list[dict]:
    with open(QUESTIONS_PATH) as f:
        return json.load(f)


def eval_retrieval(top_k: int = 5) -> dict:
    """Evaluate retrieval recall@k. Does the right source show up?"""
    from src.retrieval.retriever import retrieve

    questions = load_questions()
    hits = 0
    total = len(questions)
    per_question = []

    for q in questions:
        results = retrieve(q["question"], top_k=top_k)
        retrieved_sources = [r["source"] for r in results]
        retrieved_texts = " ".join(r["text"].lower() for r in results)

        # check if any relevant source was retrieved
        source_hit = any(
            src in retrieved_sources for src in q["relevant_sources"]
        )

        # also check keyword overlap
        keyword_hits = sum(
            1 for kw in q["relevant_keywords"]
            if kw.lower() in retrieved_texts
        )
        keyword_recall = keyword_hits / len(q["relevant_keywords"])

        hit = source_hit and keyword_recall >= 0.3
        if hit:
            hits += 1

        per_question.append({
            "id": q["id"],
            "question": q["question"][:60],
            "source_hit": source_hit,
            "keyword_recall": round(keyword_recall, 2),
            "hit": hit,
        })

    recall = hits / total
    logger.info(f"retrieval recall@{top_k}: {recall:.3f} ({hits}/{total})")
    return {
        "recall_at_k": round(recall, 3),
        "top_k": top_k,
        "hits": hits,
        "total": total,
        "per_question": per_question,
    }


def eval_generation() -> dict:
    """Evaluate end-to-end RAG: retrieve + generate + check answer."""
    from src.generation.generator import check_ollama, generate
    from src.generation.prompt import format_prompt
    from src.retrieval.retriever import retrieve

    if not check_ollama():
        logger.error("ollama not available, skipping generation eval")
        return {"error": "ollama not available"}

    questions = load_questions()
    results = []
    latencies = []

    for q in questions:
        chunks = retrieve(q["question"], top_k=5)
        prompt = format_prompt(q["question"], chunks)

        t0 = time.time()
        gen = generate(prompt)
        latency = time.time() - t0
        latencies.append(latency)

        answer = gen["answer"].lower()
        expected_keywords = q["relevant_keywords"]

        # simple keyword overlap scoring
        matched = sum(1 for kw in expected_keywords if kw.lower() in answer)
        correctness = matched / len(expected_keywords)

        results.append({
            "id": q["id"],
            "question": q["question"][:60],
            "correctness": round(correctness, 2),
            "latency_s": round(latency, 2),
        })

    avg_correctness = sum(r["correctness"] for r in results) / len(results)
    avg_latency = sum(latencies) / len(latencies)

    logger.info(f"avg correctness: {avg_correctness:.3f}")
    logger.info(f"avg latency: {avg_latency:.1f}s")

    return {
        "avg_correctness": round(avg_correctness, 3),
        "avg_latency_s": round(avg_latency, 2),
        "per_question": results,
    }


def main():
    logger.info("=== retrieval evaluation ===")
    ret_results = eval_retrieval(top_k=5)

    logger.info("=== generation evaluation ===")
    gen_results = eval_generation()

    # save results
    out = {
        "retrieval": ret_results,
        "generation": gen_results,
    }
    out_path = Path("evaluation/results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    logger.info(f"saved results to {out_path}")


if __name__ == "__main__":
    main()
