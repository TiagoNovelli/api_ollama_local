from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agents.support_agent import build_support_agent


class SupportState(TypedDict):
    user_input: str
    answer: str


def run_support_agent(state: SupportState) -> SupportState:
    agent = build_support_agent()
    result = agent.invoke(
        {"messages": [{"role": "user", "content": state["user_input"]}]}
    )
    messages = result.get("messages", [])
    if messages:
        content = getattr(messages[-1], "content", str(messages[-1]))
    else:
        content = str(result)
    return {"user_input": state["user_input"], "answer": content}


graph = StateGraph(SupportState)
graph.add_node("support_agent", run_support_agent)
graph.add_edge(START, "support_agent")
graph.add_edge("support_agent", END)
support_graph = graph.compile()


if __name__ == "__main__":
    output = support_graph.invoke({"user_input": "Procure no catalogo por mesa"})
    print(output["answer"])
