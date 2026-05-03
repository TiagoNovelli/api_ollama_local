# Knowledge Base

Este diretorio guarda os documentos fonte para o RAG.

## Fluxo

1. voce adiciona arquivos aqui
2. roda `python -m rag.ingest`
3. o Chroma indexa os chunks em `vector_store/`
4. o endpoint `/agents/rag-support` passa a recuperar esse contexto

## Formatos aceitos

- `.md`
- `.txt`
- `.rst`
- `.json`
