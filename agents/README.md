# Agents

Agentes sao componentes que usam um modelo, contexto e ferramentas para decidir o que fazer em uma tarefa.

## Diferenca entre agente e skill

- agente: decide o proximo passo
- skill: executa uma capacidade especifica

## Em pratica

Um agente normalmente junta:

- modelo
- prompt
- ferramentas
- memoria ou estado
- regras de parada

## Agentes deste projeto

- `support_agent.py`: agente focado em suporte e catalogo local
- `research_agent.py`: agente focado em busca e leitura de paginas com Firecrawl

## Quando usar mais de um agente

Crie mais de um agente quando cada um tiver:

- ferramentas diferentes
- objetivos diferentes
- prompts muito diferentes
- niveis de autonomia diferentes
