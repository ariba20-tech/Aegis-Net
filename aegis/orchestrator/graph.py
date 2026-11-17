"""
LangGraph Central Orchestrator & Cyclic State Machine
Owner: Ariba Hurrain Hussain
Builds and compiles the cyclic execution workflow for AEGIS-NET.
"""

from langgraph.graph import StateGraph, START, END
from aegis.contracts.state import EncounterState
from aegis.orchestrator.nodes import (
    intake_node,
    agents_node,
    evaluation_node,
    retry_node,
    reporting_node,
)
from aegis.orchestrator.router import AgentRouter


def build_aegis_graph() -> StateGraph:
    """
    Constructs the AEGIS-NET cyclic multi-agent workflow:
    START -> intake_node -> agents_node -> evaluation_node -> [conditional retry router]
      - if retry needed: retry_node -> agents_node (cycle)
      - if verified: reporting_node -> END
    """
    workflow = StateGraph(EncounterState)

    # 1. Add Workflow Nodes
    workflow.add_node("intake_node", intake_node)
    workflow.add_node("agents_node", agents_node)
    workflow.add_node("evaluation_node", evaluation_node)
    workflow.add_node("retry_node", retry_node)
    workflow.add_node("reporting_node", reporting_node)

    # 2. Add Linear Edges
    workflow.add_edge(START, "intake_node")
    workflow.add_edge("intake_node", "agents_node")
    workflow.add_edge("agents_node", "evaluation_node")

    # 3. Add Conditional Cyclic Edge from evaluation_node
    workflow.add_conditional_edges(
        "evaluation_node",
        AgentRouter.should_retry,
        {
            "retry_node": "retry_node",
            "reporting_node": "reporting_node"
        }
    )

    # 4. Cycle retry_node back to agents_node
    workflow.add_edge("retry_node", "agents_node")

    # 5. Connect reporting_node to completion
    workflow.add_edge("reporting_node", END)

    return workflow


def get_compiled_orchestrator():
    """Returns the compiled, runnable LangGraph application."""
    workflow = build_aegis_graph()
    return workflow.compile()

