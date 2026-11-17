"""
Encounter Memory & Context Management
Owner: Ariba Hurrain Hussain
Maintains patient context, prior encounter summaries, and iteration history across cyclic passes.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class EncounterMemory:
    """Manages short-term (in-encounter cyclic passes) and long-term (patient longitudinal) context."""

    def __init__(self, patient_id: str, encounter_id: str):
        self.patient_id = patient_id
        self.encounter_id = encounter_id
        self.history: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "iterations_recorded": 0
        }

    def record_iteration(self, iteration: int, findings_count: int, critic_notes: str, needs_retry: bool):
        """Snapshots each pass of the cyclic orchestrator for historical traceability."""
        self.history.append({
            "iteration": iteration,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "findings_count": findings_count,
            "critic_notes": critic_notes,
            "needs_retry": needs_retry
        })
        self.metadata["iterations_recorded"] = len(self.history)

    def get_summary(self) -> Dict[str, Any]:
        """Provides high-level context back to the LangGraph state."""
        return {
            "patient_id": self.patient_id,
            "encounter_id": self.encounter_id,
            "total_passes": len(self.history),
            "pass_history": self.history
        }

