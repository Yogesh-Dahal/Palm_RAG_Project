from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.nodes import intent_node, rag_node, booking_node
from router.rag import route

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("intent", intent_node)
    graph.add_node("qa", rag_node)
    graph.add_node("booking", booking_node)

    graph.set_entry_point("intent")

    graph.add_conditional_edges(
        "intent",
        route,
        {
            "qa": "qa",
            "booking": "booking"
        }
    )

    graph.add_edge("qa", END)
    graph.add_edge("booking", END)

    return graph.compile()
