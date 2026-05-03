from rag.retriever import query_knowledge


def search_knowledge_base(question: str, top_k: int = 4) -> str:
    """Search the local knowledge base and return formatted chunks."""
    results = query_knowledge(question, top_k=top_k)
    if not results:
        return "No relevant knowledge found."

    lines = []
    for item in results:
        lines.append(f"Source: {item['source']}\n{item['content']}")
    return "\n\n".join(lines)
