from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import time
import requests

load_dotenv()

APP_VERSION = "1.0.0"
API_TOKEN = os.getenv("API_TOKEN", "")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

app = FastAPI(
    title="API Ollama Local",
    version=APP_VERSION,
    description="Camada compatível com OpenAI para um servidor Ollama local.",
)


class ChatBody(BaseModel):
    prompt: str
    model: str | None = None


class OpenAIMessage(BaseModel):
    role: str
    content: str


class OpenAIChatRequest(BaseModel):
    model: str | None = None
    messages: list[OpenAIMessage]
    stream: bool = False


def require_bearer(authorization: str | None) -> None:
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")


def openai_error(status_code: int, message: str, error_type: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "message": message,
                "type": error_type,
            }
        },
    )


def pseudo_tokens(text: str) -> int:
    return len(text.strip().split()) if text.strip() else 0


def pseudo_tokens_from_messages(messages: list[OpenAIMessage]) -> int:
    total = 0
    for item in messages:
        total += pseudo_tokens(item.role)
        total += pseudo_tokens(item.content)
    return total


@app.get("/health")
def health():
    return {"ok": True, "version": APP_VERSION, "model": OLLAMA_MODEL}


@app.get("/version")
def version():
    return {"version": APP_VERSION}


@app.get("/v1/models")
def list_models(authorization: str | None = Header(default=None)):
    require_bearer(authorization)
    return {
        "object": "list",
        "data": [
            {
                "id": OLLAMA_MODEL,
                "object": "model",
                "created": 0,
                "owned_by": "ollama",
            }
        ],
    }


@app.post("/chat")
def chat(body: ChatBody, authorization: str | None = Header(default=None)):
    require_bearer(authorization)

    model = body.model or OLLAMA_MODEL
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": model,
            "prompt": body.prompt,
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.json()


@app.post("/v1/chat/completions")
def chat_completions(body: OpenAIChatRequest, authorization: str | None = Header(default=None)):
    require_bearer(authorization)

    if body.stream:
        return openai_error(400, "stream=true is not supported", "invalid_request_error")

    if not body.messages:
        return openai_error(400, "messages are required", "invalid_request_error")

    model = body.model or OLLAMA_MODEL
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "messages": [message.model_dump() for message in body.messages],
            "stream": False,
        },
        timeout=180,
    )

    try:
        response.raise_for_status()
    except requests.HTTPError:
        try:
            payload = response.json()
            message = payload.get("error", response.text)
        except ValueError:
            message = response.text
        return openai_error(502, message or "upstream error", "server_error")

    payload = response.json()
    content = payload.get("message", {}).get("content", "")
    prompt_tokens = pseudo_tokens_from_messages(body.messages)
    completion_tokens = pseudo_tokens(content)

    return {
        "id": f"chatcmpl-{time.time_ns()}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }
