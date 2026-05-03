from pathlib import Path
from typing import Any
import hashlib
import json

import chromadb
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings


SUPPORTED_EXTENSIONS = {".md", ".txt", ".rst", ".json"}


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _knowledge_dir() -> Path:
    path = Path(settings.knowledge_dir)
    return path if path.is_absolute() else _project_root() / path


def _chroma_dir() -> Path:
    path = Path(settings.chroma_dir)
    return path if path.is_absolute() else _project_root() / path


def _client() -> chromadb.PersistentClient:
    chroma_dir = _chroma_dir()
    chroma_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(chroma_dir))


def _collection():
    return _client().get_or_create_collection(name=settings.chroma_collection)


def _embed_texts(texts: list[str]) -> list[list[float]]:
    response = requests.post(
        f"{settings.ollama_url}/api/embed",
        json={"model": settings.embedding_model, "input": texts},
        timeout=180,
    )
    response.raise_for_status()
    payload = response.json()
    embeddings = payload.get("embeddings")
    if embeddings:
        return embeddings
    embedding = payload.get("embedding")
    if embedding:
        return [embedding]
    raise RuntimeError("No embeddings returned by Ollama.")


def _load_source_documents() -> list[dict[str, str]]:
    knowledge_dir = _knowledge_dir()
    documents: list[dict[str, str]] = []
    for path in knowledge_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        content = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".json":
            try:
                content = json.dumps(json.loads(content), ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                pass
        documents.append(
            {
                "source": str(path.relative_to(_project_root())),
                "content": content,
            }
        )
    return documents


def _chunk_documents(documents: list[dict[str, str]]) -> list[dict[str, str]]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
    chunks: list[dict[str, str]] = []
    for document in documents:
        for index, chunk in enumerate(splitter.split_text(document["content"])):
            chunk_id = hashlib.sha1(f"{document['source']}::{index}::{chunk}".encode("utf-8")).hexdigest()
            chunks.append(
                {
                    "id": chunk_id,
                    "source": document["source"],
                    "content": chunk,
                }
            )
    return chunks


def rebuild_collection() -> dict[str, Any]:
    client = _client()
    try:
        client.delete_collection(settings.chroma_collection)
    except Exception:
        pass

    collection = client.get_or_create_collection(name=settings.chroma_collection)
    documents = _load_source_documents()
    chunks = _chunk_documents(documents)
    if not chunks:
        return {"documents": 0, "chunks": 0}

    embeddings = _embed_texts([chunk["content"] for chunk in chunks])
    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["content"] for chunk in chunks],
        metadatas=[{"source": chunk["source"]} for chunk in chunks],
        embeddings=embeddings,
    )
    return {"documents": len(documents), "chunks": len(chunks)}


def query_knowledge(question: str, top_k: int = 4) -> list[dict[str, str]]:
    if not question.strip():
        return []
    collection = _collection()
    embeddings = _embed_texts([question])
    result = collection.query(
        query_embeddings=embeddings,
        n_results=max(1, top_k),
    )
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    output = []
    for document, metadata in zip(documents, metadatas):
        output.append(
            {
                "source": metadata.get("source", "unknown"),
                "content": document,
            }
        )
    return output
