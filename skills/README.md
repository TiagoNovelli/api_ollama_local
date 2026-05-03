# Skills

Skills sao capacidades pequenas e reutilizaveis que um agente pode usar para agir no mundo.

## Em linguagem simples

- Um agente decide **o que fazer**
- Uma skill executa **como fazer**

## Exemplos de skills

- consultar a saude da API
- buscar itens em um catalogo
- raspar uma pagina web
- resumir um texto
- criar um payload de integracao

## Como pensar neste diretorio

Cada arquivo aqui deve ter uma responsabilidade clara e ser facil de testar isoladamente.

Boa regra:

- uma skill deve fazer uma coisa bem
- a entrada e a saida devem ser simples
- o agente deve conseguir chamar a skill como ferramenta

## Skills deste projeto

- `api_health.py`: verifica a saude da API publica
- `catalog_search.py`: busca em um catalogo local versionado
- `firecrawl_tools.py`: exemplos de scrape e search com Firecrawl
- `rag_search.py`: busca semantica na base de conhecimento local
