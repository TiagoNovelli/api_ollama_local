from pathlib import Path

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from config import settings
from skills.firecrawl_tools import scrape_url_as_markdown, search_web


PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "research_system.txt"


def build_research_agent():
    llm = ChatOpenAI(
        model=settings.default_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0,
    )
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    return create_agent(
        model=llm,
        tools=[search_web, scrape_url_as_markdown],
        system_prompt=system_prompt,
    )


if __name__ == "__main__":
    agent = build_research_agent()
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Pesquise Firecrawl e resuma como ele pode ajudar em scraping para LLMs.",
                }
            ]
        }
    )
    print(result)
