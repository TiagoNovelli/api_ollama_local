from pathlib import Path

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from config import settings
from skills.api_health import get_public_api_health
from skills.catalog_search import search_sample_catalog


PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "support_system.txt"


def build_support_agent():
    llm = ChatOpenAI(
        model=settings.default_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0,
    )
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    return create_agent(
        model=llm,
        tools=[get_public_api_health, search_sample_catalog],
        system_prompt=system_prompt,
    )


if __name__ == "__main__":
    agent = build_support_agent()
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Verifique a saude da API e depois procure no catalogo por sofa.",
                }
            ]
        }
    )
    print(result)
