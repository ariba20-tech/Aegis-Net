"""
AEGIS-NET End-to-End Orchestration Runner
Demonstrates the cyclic multi-agent execution pipeline.
Executed by: Ariba Hurrain Hussain (Orchestration & Integration)
"""

import json
from aegis.orchestrator.graph import get_compiled_orchestrator
from aegis.contracts.state import EncounterState


def run_sample_encounter():
    print("=" * 70)
    print("🏥 AEGIS-NET: Clinical Multimodal Multi-Agent System")
    print("=" * 70)

    # Compile Ariba's LangGraph orchestrator
    print("[1/4] Compiling Central LangGraph Orchestrator...")
    app = get_compiled_orchestrator()

    # Synthetic clinical encounter with multimodal data
    initial_state: EncounterState = {
        "patient_id": "PT-2026-9812",
        "encounter_id": "ENC-ED-4401",
        "iteration": 1,
        "max_retries": 2,
        "raw_inputs": {
            "image": "dicom/chest_cxr_pt9812.dcm",
            "ehr": (
                "67-year-old male presenting with acute fever (102.1 F), productive cough with purulent sputum, "
                "pleuritic chest pain, and progressive shortness of breath for 3 days. History of mild COPD."
            ),
            "vitals": {
                "heart_rate": 112,
                "blood_pressure": "138/84",
                "respiratory_rate": 25,
                "spo2_percent": 89,
                "temperature_f": 102.1
            }
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

    print("\n[2/4] Executing Workflow over Multimodal Encounter...")
    final_output = app.invoke(initial_state)

    print("\n[3/4] Workflow Execution Completed Successfully!")
    print(f"-> Total Iterations Run: {final_output['iteration']}")
    print(f"-> Audit Trail Steps Recorded: {len(final_output['audit_trail'])}")
    for log in final_output['audit_trail']:
        print(f"   [{log['timestamp']}] Node: {log['step']}")

    report = final_output.get("final_report")
    if report:
        print("\n" + "=" * 70)
        print("📄 FINAL CLINICAL REPORT & TRIAGE VERDICT")
        print("=" * 70)
        print(f"Patient ID:     {report.patient_id}")
        print(f"Encounter ID:   {report.encounter_id}")
        print(f"Triage Level:   🚨 [{report.triage.value}]")
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
    run_sample_encounter()
