import os

def ask(question):
    from .rag import search
    context = search(question, 5)

    try:
        import ollama
        model = os.getenv("OLLAMA_CHAT_MODEL", "llama3.2")
        context_text = "\n".join(x["text"] for x in context)
        prompt = (
            "Answer using the supplied e-commerce catalog context. "
            "If the context does not contain the answer, say that clearly.\n\n"
            f"Context:\n{context_text}\n\nQuestion: {question}"
        )
        result = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        answer = result["message"]["content"]
        provider = "ollama"
    except Exception:
        answer = (
            "AI model is unavailable, so here is the retrieved catalog context: "
            + (" | ".join(x["text"] for x in context) if context else "No matching products found.")
        )
        provider = "retrieval-fallback"

    return {
        "question": question,
        "answer": answer,
        "provider": provider,
        "sources": context,
    }
