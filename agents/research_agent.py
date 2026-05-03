from pathlib import Path
import re

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import settings
from skills.firecrawl_tools import scrape_url_as_markdown, search_web


PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "research_system.txt"
URL_PATTERN = re.compile(r"https?://\\S+")


def _llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.default_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0,
    )


def build_research_context(user_input: str) -> str:
    context_parts: list[str] = []

    urls = URL_PATTERN.findall(user_input)
    for url in urls[:1]:
        try:
            context_parts.append(scrape_url_as_markdown(url))
        except Exception as exc:  # pragma: no cover
            context_parts.append(f"Falha ao raspar {url}: {exc}")

    if not urls:
        try:
            context_parts.append(search_web(user_input))
        except Exception as exc:  # pragma: no cover
            context_parts.append(f"Falha ao pesquisar na web: {exc}")

    if not context_parts:
        context_parts.append("Nenhuma fonte externa foi consultada.")
    return "\n\n".join(context_parts)


def run_research_agent(user_input: str) -> str:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    context = build_research_context(user_input)
    user_prompt = (
        f"Pedido do usuario:\n{user_input}\n\n"
        f"Contexto coletado pelas skills:\n{context}\n\n"
        "Responda em portugues do Brasil com um resumo curto e util."
    )
    response = _llm().invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )
    return response.content if isinstance(response.content, str) else str(response.content)


def build_research_agent():
    return run_research_agent


if __name__ == "__main__":
    result = run_research_agent("Pesquise Firecrawl e resuma como ele pode ajudar em scraping para LLMs.")
    print(result)
