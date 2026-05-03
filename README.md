# API Ollama Local

Camada simples em `FastAPI` para expor um servidor `Ollama` local com compatibilidade basica com a API da OpenAI.

Este repositorio tambem inclui uma estrutura inicial para:

- agentes com `LangChain`
- workflows com `LangGraph`
- skills reutilizaveis
- scraping e search com `Firecrawl`
- RAG com `ChromaDB`

## Versao

`1.1.0`

## Recursos

- `GET /health`
- `GET /version`
- `GET /v1/models`
- `POST /chat`
- `POST /v1/chat/completions`
- `POST /agents/rag-support`
- exemplos de agentes e skills versionaveis
- exemplos de workflow com LangGraph
- ingestao local de documentos para RAG

## Requisitos

- Python 3.10+
- Ollama rodando localmente

## O que sao agentes e skills

### Agentes

Agentes sao componentes que usam um modelo, contexto e ferramentas para decidir o proximo passo.

Exemplos:

- entender uma pergunta
- decidir se precisa consultar uma ferramenta
- combinar resposta do modelo com dados externos

### Skills

Skills sao capacidades pequenas e reutilizaveis que um agente pode chamar.

Exemplos:

- verificar a saude da API
- buscar um item no catalogo
- raspar uma URL com Firecrawl
- consultar a base vetorial do projeto

Regra pratica:

- agente decide
- skill executa

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
OPENAI_BASE_URL=https://ollama.brainess.com.br/v1
OPENAI_API_KEY=troque-este-token
DEFAULT_MODEL=qwen2.5:3b
FIRECRAWL_API_KEY=
EMBEDDING_MODEL=nomic-embed-text
CHROMA_DIR=./vector_store/chroma
CHROMA_COLLECTION=knowledge_base
KNOWLEDGE_DIR=./data/knowledge
```

## Dependencias para agentes

Este projeto inclui dependencias para:

- `openai`
- `langchain`
- `langchain-openai`
- `langgraph`
- `firecrawl-py`
- `chromadb`

## Executando localmente

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

## URL publica atual

Se a API estiver publicada pelo seu tunel/proxy, a URL publica usada hoje e:

```text
https://ollama.brainess.com.br
```

## Estrutura do projeto

```text
api_ollama_local/
  agents/
  skills/
  workflows/
  prompts/
  data/
  rag/
  examples/
  app.py
  config.py
  requirements.txt
  .env.example
```

## Diretorios importantes

- `agents/`: agentes prontos e documentados
- `skills/`: ferramentas reutilizaveis
- `workflows/`: fluxos com LangGraph
- `prompts/`: prompts versionados
- `data/`: catalogo e fixtures pequenas
- `examples/`: exemplos rapidos para testar
- `rag/`: ingestao e recuperacao vetorial

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
  "version": "1.1.0",
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

### RAG Support

Antes de usar, faca a ingestao da base:

```bash
python -m examples.ingest_knowledge
```

Local:

```bash
curl http://127.0.0.1:8000/agents/rag-support \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Quais sofas existem no catalogo de exemplo?",
    "top_k": 3
  }'
```

Publico:

```bash
curl https://ollama.brainess.com.br/agents/rag-support \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Quais sofas existem no catalogo de exemplo?",
    "top_k": 3
  }'
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

## Exemplos de agentes e workflows

Rode a partir da raiz do repositorio:

```bash
python -m examples.use_openai_sdk
python -m examples.ingest_knowledge
python -m agents.support_agent
python -m agents.rag_support_agent
python -m workflows.support_graph
```

Se voce tiver `FIRECRAWL_API_KEY` configurada:

```bash
python -m agents.research_agent
```

## Como versionar bem agentes e skills

Versione no Git:

- codigo Python
- prompts
- schemas
- catalogos pequenos
- exemplos
- testes

Nao versione:

- `.env`
- segredos
- caches
- logs
- bases grandes geradas em runtime

O diretorio `vector_store/` fica no `.gitignore` porque e gerado pela ingestao do Chroma.

## Observacoes

- `stream=true` ainda nao esta implementado.
- `GET /v1/models` retorna o modelo padrao configurado no `.env`.
- O token e validado via header `Authorization: Bearer ...`.
- O RAG usa `EMBEDDING_MODEL` para gerar embeddings via Ollama.
