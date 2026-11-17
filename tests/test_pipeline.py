"""
Unit and Integration Tests for AEGIS-NET
Validates contracts, orchestrator routing, and cyclic retries.
"""

import pytest
from aegis.orchestrator.graph import get_compiled_orchestrator
from aegis.contracts.state import EncounterState
from aegis.contracts.findings import ModalityType, SeverityLevel, ClinicalFinding
from aegis.contracts.evaluation import TriageLevel, DoctorCriticVerdict
from aegis.orchestrator.router import AgentRouter


def test_contracts_initialization():
    finding = ClinicalFinding(
        finding_id="F-TEST-001",
        modality=ModalityType.VISION,
        concept_name="Consolidation",
        observation="Test observation",
        confidence=0.95,
        severity=SeverityLevel.MODERATE
    )
    assert finding.finding_id == "F-TEST-001"
    assert finding.confidence == 0.95


def test_router_retry_decision():
    # Case 1: Needs retry
    state_retry: EncounterState = {
        "patient_id": "P1",
        "encounter_id": "E1",
        "iteration": 1,
        "max_retries": 2,
        "raw_inputs": {},
        "encounter_context": {},
        "agent_reports": [],
        "accumulated_findings": [],
        "conflicts": [],
        "critic_verdict": DoctorCriticVerdict(
            is_plausible=True,
            hallucination_detected=False,
            guideline_concordant=True,
            verification_confidence=0.60,
            critique_notes="Needs clarification",
            needs_retry=True,
            retry_guidance="Focus on RLL"
        ),
        "retry_targets": [],
        "retry_prompt": None,
        "triage_level": None,
        "final_report": None,
        "audit_trail": []
    }
    decision = AgentRouter.should_retry(state_retry)
    assert decision == "retry_node"

    # Case 2: Max retries exceeded -> proceed to reporting
    state_retry["iteration"] = 3
    decision_max = AgentRouter.should_retry(state_retry)
    assert decision_max == "reporting_node"


def test_end_to_end_graph_execution():
    app = get_compiled_orchestrator()
    sample_state: EncounterState = {
        "patient_id": "PT-TEST-001",
        "encounter_id": "ENC-TEST-001",
        "iteration": 1,
        "max_retries": 2,
        "raw_inputs": {
            "image": "dummy_path.dcm",
            "ehr": "Patient with cough and fever.",
            "vitals": {"spo2": 91}
        },
        "encounter_context": {},
        "agent_reports": [],
        "accumulated_findings": [],
        "conflicts": [],
        "critic_verdict": None,
        "retry_targets": [],
        "retry_prompt": None,
        "triage_level": None,
        "final_report": None,
        "audit_trail": []
    }
    result = app.invoke(sample_state)
    assert result["final_report"] is not None
    assert result["triage_level"] in (TriageLevel.RED, TriageLevel.YELLOW, TriageLevel.GREEN)
    assert len(result["audit_trail"]) >= 4

