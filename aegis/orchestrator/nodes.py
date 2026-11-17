"""
LangGraph Execution Nodes
Owner: Ariba Hurrain Hussain
Wraps Sanjoli's ingestion agents and Padmini's evaluation components into LangGraph-compatible node functions.
"""

from typing import Dict, Any, List
from aegis.contracts.state import EncounterState
from aegis.contracts.findings import AgentFindingReport, ClinicalFinding
from aegis.contracts.evaluation import ConflictItem, DoctorCriticVerdict, TriageLevel, FinalClinicalReport
from aegis.orchestrator.memory import EncounterMemory

# Importing specialized agents from Sanjoli's module
from aegis.ingestion.vision_agent import VisionAgent
from aegis.ingestion.ehr_agent import EHRAgent
from aegis.ingestion.vitals_agent import VitalsAgent

# Importing safety & evaluation components from Padmini's module
from aegis.evaluation.debate_engine import DebateEngine
from aegis.evaluation.doctor_critic import DoctorCritic
from aegis.evaluation.triage import TriageEngine
from aegis.evaluation.report_generator import ReportGenerator
from aegis.evaluation.audit_logger import AuditLogger

# Instantiate module instances
vision_agent = VisionAgent()
ehr_agent = EHRAgent()
vitals_agent = VitalsAgent()

debate_engine = DebateEngine()
doctor_critic = DoctorCritic(confidence_threshold=0.85)
triage_engine = TriageEngine()
report_generator = ReportGenerator()


def intake_node(state: EncounterState) -> Dict[str, Any]:
    """Initializes encounter memory, sets default context, and prepares agent routing."""
    patient_id = state["patient_id"]
    encounter_id = state["encounter_id"]
    
    memory = EncounterMemory(patient_id, encounter_id)
    audit_entry = AuditLogger.create_log_entry("intake_node", {
        "status": "initialized",
        "patient_id": patient_id,
        "encounter_id": encounter_id
    })

    return {
        "iteration": 1,
        "encounter_context": memory.get_summary(),
        "audit_trail": [audit_entry]
    }


def agents_node(state: EncounterState) -> Dict[str, Any]:
    """
    Invokes specialized multimodal agents (Vision, EHR, Vitals) concurrently or in sequence.
    Applies retry prompts if cycling back.
    """
    raw_inputs = state.get("raw_inputs", {})
    context = state.get("encounter_context", {})
    retry_prompt = state.get("retry_prompt")
    iteration = state.get("iteration", 1)

    reports: List[AgentFindingReport] = []
    new_findings: List[ClinicalFinding] = []

    # 1. Vision Agent (Sanjoli)
    if "image" in raw_inputs:
        v_report = vision_agent.analyze(raw_inputs["image"], context=context, retry_hint=retry_prompt)
        reports.append(v_report)
        new_findings.extend(v_report.findings)

    # 2. EHR Agent (Sanjoli)
    if "ehr" in raw_inputs:
        e_report = ehr_agent.analyze(raw_inputs["ehr"], context=context, retry_hint=retry_prompt)
        reports.append(e_report)
        new_findings.extend(e_report.findings)

    # 3. Vitals Agent (Sanjoli)
    if "vitals" in raw_inputs:
        vit_report = vitals_agent.analyze(raw_inputs["vitals"], context=context, retry_hint=retry_prompt)
        reports.append(vit_report)
        new_findings.extend(vit_report.findings)

    audit_entry = AuditLogger.create_log_entry("agents_node", {
        "iteration": iteration,
        "reports_count": len(reports),
        "findings_extracted": len(new_findings)
    })

    return {
        "agent_reports": reports,
        "accumulated_findings": new_findings,
        "audit_trail": [audit_entry]
    }


def evaluation_node(state: EncounterState) -> Dict[str, Any]:
    """
    Invokes Padmini's Cross-Agent Debate Engine and Doctor-Critic Verification Layer.
    """
    reports = state.get("agent_reports", [])
    findings = state.get("accumulated_findings", [])
    iteration = state.get("iteration", 1)
    max_retries = state.get("max_retries", 2)

    # 1. Cross-Agent Debate & Conflict Detection
    conflicts = debate_engine.evaluate_consensus(reports)

    # 2. Doctor-Critic Verification
    verdict = doctor_critic.verify(
        findings=findings,
        conflicts=conflicts,
        iteration=iteration,
        max_retries=max_retries
    )

    audit_entry = AuditLogger.create_log_entry("evaluation_node", {
        "iteration": iteration,
        "conflicts_detected": len(conflicts),
        "critic_confidence": verdict.verification_confidence,
        "needs_retry": verdict.needs_retry
    })

    return {
        "conflicts": conflicts,
        "critic_verdict": verdict,
        "audit_trail": [audit_entry]
    }


def retry_node(state: EncounterState) -> Dict[str, Any]:
    """
    Handles state transition when Doctor-Critic demands a cyclic re-evaluation.
    Increments iteration and passes critic guidance to specialized agents.
    """
    current_iter = state.get("iteration", 1)
    critic = state.get("critic_verdict")
    retry_prompt = critic.retry_guidance if critic else "Re-evaluate ambiguous clinical signals."

    audit_entry = AuditLogger.create_log_entry("retry_node", {
        "transitioning_to_iteration": current_iter + 1,
        "retry_guidance": retry_prompt
    })

    return {
        "iteration": current_iter + 1,
        "retry_prompt": retry_prompt,
        "audit_trail": [audit_entry]
    }


def reporting_node(state: EncounterState) -> Dict[str, Any]:
    """
    Invokes Padmini's Triage Engine and builds the Final Clinical Report & FHIR bundle.
    """
    patient_id = state["patient_id"]
    encounter_id = state["encounter_id"]
    findings = state.get("accumulated_findings", [])
    verdict = state.get("critic_verdict")

    # 1. Triage Classification
    triage = triage_engine.classify(findings)

    # 2. Final Report Generation
    report = report_generator.build_report(
        patient_id=patient_id,
        encounter_id=encounter_id,
        findings=findings,
        verdict=verdict,
        triage=triage
    )

    audit_entry = AuditLogger.create_log_entry("reporting_node", {
        "triage": triage.value,
        "trace_id": report.audit_trace_id,
        "diagnoses": report.synthesized_diagnosis
    })

    return {
        "triage_level": triage,
        "final_report": report,
        "audit_trail": [audit_entry]
    }

