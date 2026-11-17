"""
Agent Routing & Conditional Edge Logic
Owner: Ariba Hurrain Hussain
Implements dynamic routing and retry decisions for LangGraph conditional branches.
"""

from typing import Literal
from aegis.contracts.state import EncounterState


class AgentRouter:
    """Decides the execution path through the LangGraph workflow."""

    @staticmethod
    def should_retry(state: EncounterState) -> Literal["retry_node", "reporting_node"]:
        """
        Evaluates the DoctorCriticVerdict and current iteration counter.
        Returns 'retry_node' to cycle back to specialized agents with guidance,
        or 'reporting_node' to finalize clinical documentation.
        """
        critic = state.get("critic_verdict")
        iteration = state.get("iteration", 1)
        max_retries = state.get("max_retries", 2)

        if critic and critic.needs_retry and iteration <= max_retries:
            return "retry_node"

        return "reporting_node"
