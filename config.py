from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_token: str = os.getenv("API_TOKEN", "")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://ollama.brainess.com.br/v1")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", os.getenv("API_TOKEN", ""))
    default_model: str = os.getenv("DEFAULT_MODEL", os.getenv("OLLAMA_MODEL", "qwen2.5:3b"))
    firecrawl_api_key: str = os.getenv("FIRECRAWL_API_KEY", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    chroma_dir: str = os.getenv("CHROMA_DIR", "./vector_store/chroma")
    chroma_collection: str = os.getenv("CHROMA_COLLECTION", "knowledge_base")
    knowledge_dir: str = os.getenv("KNOWLEDGE_DIR", "./data/knowledge")


settings = Settings()
