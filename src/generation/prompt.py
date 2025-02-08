"""RAG prompt templates."""

RAG_TEMPLATE = """Use the following context to answer the question. If the context doesn't contain enough information, say so. Don't make things up.

Context:
{context}

Question: {question}

Answer:"""


RAG_TEMPLATE_CONCISE = """Answer the question based only on the provided context. Be concise.

Context:
{context}

Question: {question}

Answer:"""


def format_prompt(
    question: str,
    chunks: list[dict],
    template: str = RAG_TEMPLATE,
) -> str:
    context = "\n\n---\n\n".join(
        f"[{c['source']} p.{c['page']}]\n{c['text']}" for c in chunks
    )
    return template.format(context=context, question=question)
