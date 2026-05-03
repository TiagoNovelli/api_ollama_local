from rag.retriever import rebuild_collection


def rebuild_knowledge_index() -> dict[str, int]:
    return rebuild_collection()


if __name__ == "__main__":
    result = rebuild_knowledge_index()
    print(f"Indexed {result['documents']} documents into {result['chunks']} chunks.")
