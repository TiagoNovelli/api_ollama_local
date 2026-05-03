from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import settings
from rag.retriever import query_knowledge


PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "rag_support_system.txt"


def _llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.default_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0,
    )


def retrieve_rag_context(question: str, top_k: int = 4) -> list[dict[str, str]]:
    return query_knowledge(question, top_k=top_k)


def run_rag_support_agent(question: str, top_k: int = 4) -> dict[str, object]:
    results = retrieve_rag_context(question, top_k=top_k)
    context = "\n\n".join(
        f"Source: {item['source']}\n{item['content']}" for item in results
    )
    if not context:
        context = "No relevant context was retrieved from the knowledge base."

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    user_prompt = (
        f"Pergunta do usuario:\n{question}\n\n"
        f"Contexto recuperado do banco vetorial:\n{context}\n\n"
        "Responda com base no contexto. Se ele nao for suficiente, diga isso claramente."
    )
    response = _llm().invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )
    answer = response.content if isinstance(response.content, str) else str(response.content)
    return {
        "answer": answer,
        "sources": [item["source"] for item in results],
        "chunks": results,
    }


if __name__ == "__main__":
    print(run_rag_support_agent("Quais modelos de sofa existem no catalogo de exemplo?"))
