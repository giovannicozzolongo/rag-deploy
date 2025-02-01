"""Streamlit chat interface for the RAG system."""

import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Doc Search", layout="wide")
st.title("Doc Search")
st.caption("Ask questions about Python stdlib and scikit-learn docs")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            try:
                resp = requests.post(
                    f"{API_URL}/query",
                    json={"question": prompt, "top_k": 5},
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()

                st.markdown(data["answer"])

                with st.expander("Sources"):
                    for src in data["sources"]:
                        st.markdown(
                            f"**{src['source']}** (p.{src['page']}, score: {src['score']:.3f})"
                        )
                        st.text(src["text"][:200] + "...")

                st.caption(f"Model: {data['model']} | Latency: {data['latency_s']}s")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": data["answer"],
                    }
                )

            except requests.exceptions.ConnectionError:
                st.error("Can't reach the API. Is the backend running?")
            except Exception as e:
                st.error(f"Error: {e}")

with st.sidebar:
    st.header("About")
    st.markdown(
        "RAG system over Python stdlib and scikit-learn documentation. "
        "Uses FAISS for retrieval and Mistral-7B for generation."
    )

    # health check
    try:
        h = requests.get(f"{API_URL}/health", timeout=5).json()
        st.success(f"API: {h['status']}")
        st.info(f"Index: {'loaded' if h['index_loaded'] else 'missing'}")
        st.info(f"Ollama: {'ok' if h['ollama_available'] else 'down'}")
    except Exception:
        st.warning("API not reachable")
