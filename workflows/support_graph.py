from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agents.support_agent import run_support_agent as run_support_agent_task


class SupportState(TypedDict):
    user_input: str
    answer: str


def run_support_agent_node(state: SupportState) -> SupportState:
    content = run_support_agent_task(state["user_input"])
    return {"user_input": state["user_input"], "answer": content}


graph = StateGraph(SupportState)
graph.add_node("support_agent", run_support_agent_node)
graph.add_edge(START, "support_agent")
graph.add_edge("support_agent", END)
support_graph = graph.compile()


if __name__ == "__main__":
    output = support_graph.invoke({"user_input": "Procure no catalogo por mesa"})
    print(output["answer"])
