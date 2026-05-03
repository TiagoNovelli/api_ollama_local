# Workflows

Workflows organizam como agentes e passos deterministicos se conectam.

## Onde entra o LangGraph

LangGraph e util quando voce quer:

- estado entre etapas
- roteamento claro
- mistura de passos deterministicos com comportamento agentico
- memoria e intervencao humana no futuro

## Quando criar um workflow

Use um workflow quando um agente sozinho ja nao basta.

Exemplos:

- classificar a intencao e depois chamar um agente especifico
- executar validacoes antes de chamar o modelo
- combinar coleta de contexto, agente e pos-processamento

## Arquivo atual

- `support_graph.py`: fluxo simples que injeta uma mensagem em um agente de suporte
