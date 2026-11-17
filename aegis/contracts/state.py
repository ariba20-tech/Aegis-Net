"""
AEGIS-NET Central Orchestration State: LangGraph State Contract
Maintained by Ariba's Central LangGraph Orchestrator.
Uses typed state reducers to accumulate findings, audit logs, and cyclic iterations.
"""

from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator
from aegis.contracts.findings import ClinicalFinding, AgentFindingReport
from aegis.contracts.evaluation import DoctorCriticVerdict, ConflictItem, TriageLevel, FinalClinicalReport


def merge_dicts(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """Helper reducer to merge dictionary updates cleanly."""
    res = dict(a or {})
    if b:
        res.update(b)
    return res


class EncounterState(TypedDict):
    """
    Central LangGraph State for AEGIS-NET.
    Flows across Ingestion -> Agents -> Debate -> Critic -> Retry / Triage -> Output.
    """
    # Encounter Metadata
    patient_id: str
    encounter_id: str
    iteration: int
    max_retries: int
    
    # Input Modality Data / References
    raw_inputs: Dict[str, Any]
    
    # Context & Encounter Memory
    encounter_context: Dict[str, Any]
    
    # Agent Findings (Accumulated using operator.add)
    agent_reports: Annotated[List[AgentFindingReport], operator.add]
    accumulated_findings: Annotated[List[ClinicalFinding], operator.add]
    
    # Evaluation & Critic State
    conflicts: List[ConflictItem]
    critic_verdict: Optional[DoctorCriticVerdict]
    
    # Routing & Retry Directives
    retry_targets: List[str]  # e.g., ['vision', 'ehr'] if only specific agents should retry
    retry_prompt: Optional[str]
    
    # Final Deliverables
    triage_level: Optional[TriageLevel]
    final_report: Optional[FinalClinicalReport]
    
    # Audit Trail (Traceability log)
    audit_trail: Annotated[List[Dict[str, Any]], operator.add]
