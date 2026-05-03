from config import settings
import requests


def get_public_api_health() -> str:
    """Check whether the public API is healthy."""
    url = settings.openai_base_url.removesuffix("/v1") + "/health"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    payload = response.json()
    return f"API health: ok={payload.get('ok')} version={payload.get('version')} model={payload.get('model')}"
