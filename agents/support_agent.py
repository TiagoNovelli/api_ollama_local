from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import settings
from skills.api_health import get_public_api_health
from skills.catalog_search import search_sample_catalog


PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "support_system.txt"


def _llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.default_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0,
    )


def build_support_context(user_input: str) -> str:
    normalized = user_input.lower()
    context_parts: list[str] = []

    if any(token in normalized for token in ["health", "saude", "status", "api"]):
        context_parts.append(get_public_api_health())

    if any(
        token in normalized
        for token in ["catalogo", "catálogo", "sofa", "sofá", "mesa", "cadeira", "poltrona", "puff"]
    ):
        context_parts.append(search_sample_catalog(user_input))

    if not context_parts:
        context_parts.append("Nenhuma skill especifica foi acionada. Responda apenas com base na pergunta do usuario.")

    return "\n\n".join(context_parts)


def run_support_agent(user_input: str) -> str:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    context = build_support_context(user_input)
    user_prompt = (
        f"Pergunta do usuario:\n{user_input}\n\n"
        f"Contexto coletado pelas skills:\n{context}\n\n"
        "Responda de forma util e objetiva. Se houver resultados de catalogo, cite os itens encontrados."
    )
    response = _llm().invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )
    return response.content if isinstance(response.content, str) else str(response.content)


def build_support_agent():
    return run_support_agent


if __name__ == "__main__":
    result = run_support_agent("Verifique a saude da API e depois procure no catalogo por sofa.")
    print(result)
