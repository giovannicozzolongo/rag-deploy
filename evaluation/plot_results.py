"""Generate evaluation plots from results."""

import json
import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RESULTS_PATH = Path("evaluation/results.json")
FIGURES_DIR = Path("figures")


def load_results() -> dict:
    with open(RESULTS_PATH) as f:
        return json.load(f)


def plot_retrieval_recall(results: dict):
    """Bar chart of per-question retrieval results."""
    ret = results["retrieval"]["per_question"]
    ids = [r["id"] for r in ret]
    kw_recalls = [r["keyword_recall"] for r in ret]

    fig, ax = plt.subplots(figsize=(12, 4))
    colors = ["#2ecc71" if h else "#e74c3c" for h in [r["hit"] for r in ret]]
    ax.bar(ids, kw_recalls, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_xlabel("Question ID")
    ax.set_ylabel("Keyword Recall")
    ax.set_title(f"Retrieval Quality (recall@5 = {results['retrieval']['recall_at_k']:.2f})")
    ax.set_ylim(0, 1.1)
    ax.set_xticks(ids)
    ax.axhline(y=0.3, color="gray", linestyle="--", alpha=0.5, label="threshold")
    ax.legend()
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "retrieval_recall.png", dpi=150)
    plt.close()
    logger.info("saved retrieval_recall.png")


def plot_generation_correctness(results: dict):
    """Bar chart of per-question answer correctness."""
    gen = results["generation"]
    if "error" in gen:
        logger.warning("no generation results, skipping plot")
        return

    per_q = gen["per_question"]
    ids = [r["id"] for r in per_q]
    scores = [r["correctness"] for r in per_q]

    fig, ax = plt.subplots(figsize=(12, 4))
    colors = ["#3498db" if s >= 0.5 else "#e67e22" for s in scores]
    ax.bar(ids, scores, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_xlabel("Question ID")
    ax.set_ylabel("Answer Correctness")
    ax.set_title(f"Generation Quality (avg = {gen['avg_correctness']:.2f})")
    ax.set_ylim(0, 1.1)
    ax.set_xticks(ids)
    ax.axhline(y=0.75, color="gray", linestyle="--", alpha=0.5, label="target")
    ax.legend()
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "generation_correctness.png", dpi=150)
    plt.close()
    logger.info("saved generation_correctness.png")


def plot_latency(results: dict):
    """Latency distribution."""
    gen = results["generation"]
    if "error" in gen:
        return

    latencies = [r["latency_s"] for r in gen["per_question"]]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(latencies, bins=10, color="#9b59b6", edgecolor="white", alpha=0.8)
    ax.axvline(x=5.0, color="red", linestyle="--", label="5s target")
    avg = np.mean(latencies)
    ax.axvline(x=avg, color="green", linestyle="--", label=f"avg={avg:.1f}s")
    ax.set_xlabel("Latency (seconds)")
    ax.set_ylabel("Count")
    ax.set_title("End-to-End Response Latency")
    ax.legend()
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "latency_distribution.png", dpi=150)
    plt.close()
    logger.info("saved latency_distribution.png")


def plot_strategy_comparison(results: dict):
    """Compare chunking strategies if available."""
    if "strategy_comparison" not in results:
        return

    comp = results["strategy_comparison"]
    strategies = list(comp.keys())
    recalls = [comp[s]["recall_at_k"] for s in strategies]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(strategies, recalls, color=["#2ecc71", "#3498db", "#e67e22"])
    ax.set_ylabel("Recall@5")
    ax.set_title("Chunking Strategy Comparison")
    ax.set_ylim(0, 1.1)
    for bar, val in zip(bars, recalls):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{val:.2f}", ha="center", fontsize=11)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "strategy_comparison.png", dpi=150)
    plt.close()
    logger.info("saved strategy_comparison.png")


def main():
    FIGURES_DIR.mkdir(exist_ok=True)
    results = load_results()
    plot_retrieval_recall(results)
    plot_generation_correctness(results)
    plot_latency(results)
    plot_strategy_comparison(results)
    logger.info("all plots saved")


if __name__ == "__main__":
    main()
