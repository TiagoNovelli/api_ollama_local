# API Ollama Local

Camada simples em `FastAPI` para expor um servidor `Ollama` local com compatibilidade basica com a API da OpenAI.

## Versao

`1.0.0`

## Recursos

- `GET /health`
- `GET /version`
- `GET /v1/models`
- `POST /chat`
- `POST /v1/chat/completions`

## Requisitos

- Python 3.10+
- Ollama rodando localmente

## Instalacao

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edite o `.env`:

```env
API_TOKEN=troque-este-token
OLLAMA_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:3b
```

## Executando localmente

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

## URL publica atual

Se a API estiver publicada pelo seu tunel/proxy, a URL publica usada hoje e:

```text
https://ollama.brainess.com.br
```

## Endpoints

### Health

Local:

```bash
curl http://127.0.0.1:8000/health
```

Publico:

```bash
curl https://ollama.brainess.com.br/health
```

Resposta:

```json
{
  "ok": true,
  "version": "1.0.0",
  "model": "qwen2.5:3b"
}
```

### Models

Local:

```bash
curl http://127.0.0.1:8000/v1/models \
  -H "Authorization: Bearer SEU_TOKEN"
```

Publico:

```bash
curl https://ollama.brainess.com.br/v1/models \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Chat Completions

Local:

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:3b",
    "messages": [
      {"role": "user", "content": "Diga oi em uma frase"}
    ],
    "stream": false
  }'
```

Publico:

```bash
curl https://ollama.brainess.com.br/v1/chat/completions \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:3b",
    "messages": [
      {"role": "user", "content": "Diga oi em uma frase"}
    ],
    "stream": false
  }'
```

Resposta exemplo:

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1710000000,
  "model": "qwen2.5:3b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Ola! Como posso ajudar voce hoje?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 3,
    "completion_tokens": 6,
    "total_tokens": 9
  }
}
```

## Uso em Python

```python
from openai import OpenAI

client = OpenAI(
    api_key="SEU_TOKEN",
    base_url="https://ollama.brainess.com.br/v1",
)

response = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "Diga oi"}],
)

print(response.choices[0].message.content)
```

## Observacoes

- `stream=true` ainda nao esta implementado.
- `GET /v1/models` retorna o modelo padrao configurado no `.env`.
- O token e validado via header `Authorization: Bearer ...`.
