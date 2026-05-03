from pathlib import Path
import json


CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_catalog.json"
STOPWORDS = {
    "procure",
    "procurar",
    "catalogo",
    "catálogo",
    "por",
    "no",
    "na",
    "um",
    "uma",
    "de",
    "do",
    "da",
    "quero",
    "buscar",
}


def search_sample_catalog(query: str) -> str:
    """Search the sample catalog by keyword, category, color, or material."""
    normalized = query.strip().lower()
    if not normalized:
        return "No query provided."

    tokens = [token.strip(".,;:!?") for token in normalized.split()]
    keywords = [token for token in tokens if token and token not in STOPWORDS]
    if not keywords:
        keywords = [normalized]

    items = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    matches = []
    for item in items:
        haystack = " ".join(
            [
                item["id"],
                item["title"],
                item["category"],
                item["material"],
                item["color"],
            ]
        ).lower()
        if any(keyword in haystack for keyword in keywords):
            matches.append(item)

    if not matches:
        return "No items found in the sample catalog."

    lines = []
    for item in matches[:5]:
        lines.append(
            f"{item['id']}: {item['title']} | categoria={item['category']} | material={item['material']} | cor={item['color']} | preco={item['price']}"
        )
    return "\n".join(lines)
