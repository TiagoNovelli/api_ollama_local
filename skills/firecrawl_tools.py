from config import settings

try:
    from firecrawl import Firecrawl
except ImportError:  # pragma: no cover
    Firecrawl = None


def _client() -> "Firecrawl":
    if Firecrawl is None:
        raise RuntimeError("firecrawl-py is not installed.")
    if not settings.firecrawl_api_key:
        raise RuntimeError("FIRECRAWL_API_KEY is not configured.")
    return Firecrawl(api_key=settings.firecrawl_api_key)


def scrape_url_as_markdown(url: str) -> str:
    """Scrape a URL and return markdown content."""
    client = _client()
    result = client.scrape(url, formats=["markdown"])
    markdown = getattr(result, "markdown", None)
    if markdown:
        return markdown[:4000]
    return str(result)[:4000]


def search_web(query: str) -> str:
    """Search the web with Firecrawl and return a short text summary of results."""
    client = _client()
    result = client.search(query, limit=5)
    web_results = getattr(result, "web", [])
    if not web_results:
        return "No web results found."

    lines = []
    for item in web_results[:5]:
        title = getattr(item, "title", "Untitled")
        url = getattr(item, "url", "")
        lines.append(f"{title} - {url}")
    return "\n".join(lines)
