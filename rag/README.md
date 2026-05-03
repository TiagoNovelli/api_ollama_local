# RAG

RAG significa `Retrieval-Augmented Generation`.

## Em linguagem simples

Em vez de responder so com o que o modelo "lembra", o sistema:

1. busca trechos relevantes em uma base de conhecimento
2. injeta esse contexto no prompt
3. gera uma resposta melhor

## O que existe aqui

- `ingest.py`: le documentos e reconstrui o indice vetorial
- `retriever.py`: consulta o indice e retorna trechos relevantes

## Como usar

1. coloque arquivos em `data/knowledge/`
2. rode a ingestao
3. use o agente ou endpoint `/agents/rag-support`

## Banco vetorial usado

- `ChromaDB`

## Embeddings usados

- endpoint de embeddings do proprio Ollama, via `EMBEDDING_MODEL`
