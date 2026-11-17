"""
AEGIS-NET End-to-End Orchestration Runner
Demonstrates the cyclic multi-agent execution pipeline across benchmark encounters.
Executed by: Ariba Hurrain Hussain (Orchestration & Integration)
"""

import json
import os
import sys
from aegis.orchestrator.graph import get_compiled_orchestrator
from aegis.contracts.state import EncounterState


def load_benchmark_encounters():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sample_encounters.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []


def run_encounter(case_index: int = 0):
    print("=" * 70)
    print("🏥 AEGIS-NET: Clinical Multimodal Multi-Agent System")
    print("=" * 70)

    cases = load_benchmark_encounters()
    if not cases:
        print("[!] No benchmark cases found in data/sample_encounters.json. Using fallback.")
        return

    case = cases[case_index % len(cases)]
    print(f"\n[Case {case_index + 1}/{len(cases)}]: {case['clinical_scenario']}")
    print(f"Patient ID: {case['patient_id']} | Expected Triage: {case['expected_triage']}")

    print("\n[1/3] Compiling Central LangGraph Orchestrator...")
    app = get_compiled_orchestrator()

    initial_state: EncounterState = {
        "patient_id": case["patient_id"],
        "encounter_id": case["encounter_id"],
        "iteration": 1,
        "max_retries": 2,
        "raw_inputs": case["raw_inputs"],
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

    print("[2/3] Executing Workflow over Multimodal Encounter...")
    final_output = app.invoke(initial_state)

    print("\n[3/3] Workflow Execution Completed Successfully!")
    print(f"-> Total Iterations Run: {final_output['iteration']}")
    print(f"-> Audit Trail Steps:    {len(final_output['audit_trail'])}")

    report = final_output.get("final_report")
    if report:
        print("\n" + "=" * 70)
        print("📄 FINAL CLINICAL REPORT & TRIAGE VERDICT")
        print("=" * 70)
        print(f"Patient ID:     {report.patient_id}")
        print(f"Encounter ID:   {report.encounter_id}")
        print(f"Triage Level:   🚨 [{report.triage.value}] (Expected: {case['expected_triage']})")
        print(f"Audit Trace ID: {report.audit_trace_id}")
        print("\n🩺 Synthesized Clinical Diagnoses:")
        for diag in report.synthesized_diagnosis:
            print(f"  • {diag}")

        print("\n⚠️ Critical Findings:")
        for cf in report.critical_findings:
            print(f"  • [{cf.modality.value.upper()}] {cf.concept_name}: {cf.observation} (Confidence: {cf.confidence*100:.1f}%)")

        print("\n📋 Recommended Clinical Actions:")
        for action in report.recommended_actions:
            print(f"  • {action}")

        print("\n🩺 Doctor-Critic Verdict:")
        critic = report.critic_verdict
        print(f"  • Plausibility:           {critic.is_plausible}")
        print(f"  • Guideline Concordance:  {critic.guideline_concordant}")
        print(f"  • Verification Score:     {critic.verification_confidence*100:.1f}%")
        print(f"  • Critic Feedback:        {critic.critique_notes}")

        print("\n📦 FHIR DiagnosticReport Resource:")
        print(json.dumps(report.fhir_bundle, indent=2))
        print("=" * 70)


if __name__ == "__main__":
    idx = 0
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        idx = int(sys.argv[1])
    run_encounter(idx)
