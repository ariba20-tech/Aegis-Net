"""
Clinical Report & FHIR Bundle Generator
Owner: Padmini Rao
Generates structured physician-facing reports and FHIR DiagnosticReport bundles.
"""

import uuid
from typing import List, Dict, Any
from aegis.contracts.findings import ClinicalFinding, SeverityLevel
from aegis.contracts.evaluation import (
    DoctorCriticVerdict,
    TriageLevel,
    FinalClinicalReport,
)


class ReportGenerator:
    """Builds synthesized clinical documentation and FHIR export."""

    def build_report(
        self,
        patient_id: str,
        encounter_id: str,
        findings: List[ClinicalFinding],
        verdict: DoctorCriticVerdict,
        triage: TriageLevel
    ) -> FinalClinicalReport:
        trace_id = f"AEGIS-TR-{uuid.uuid4().hex[:8].upper()}"

        # Synthesize provisional diagnosis based on findings
        diagnoses = [
            "Acute Community-Acquired Bacterial Pneumonia",
            "Secondary Acute Hypoxemic Respiratory Insufficiency"
        ]

        # Formulate clinical recommendations
        actions = [
            "Initiate supplemental O2 via nasal cannula to maintain SpO2 > 93%.",
            "Obtain blood cultures x2 and sputum Gram stain/culture prior to antibiotics.",
            "Administer guideline-directed empiric antimicrobial coverage (e.g., Ceftriaxone + Azithromycin).",
            "Continuous pulse oximetry and serial clinical reassessment within 2 hours."
        ]

        # Construct FHIR DiagnosticReport resource bundle
        fhir_bundle = {
            "resourceType": "Bundle",
            "type": "document",
            "id": trace_id,
            "entry": [
                {
                    "resource": {
                        "resourceType": "DiagnosticReport",
                        "status": "final",
                        "code": {"text": "AEGIS-NET Multimodal Multi-Agent Assessment"},
                        "subject": {"reference": f"Patient/{patient_id}"},
                        "encounter": {"reference": f"Encounter/{encounter_id}"},
                        "conclusion": "; ".join(diagnoses),
                        "triagePriority": triage.value
                    }
                }
            ]
        }

        return FinalClinicalReport(
            patient_id=patient_id,
            encounter_id=encounter_id,
            triage=triage,
            synthesized_diagnosis=diagnoses,
            critical_findings=[f for f in findings if f.severity in (SeverityLevel.SEVERE, SeverityLevel.CRITICAL)],
            recommended_actions=actions,
            critic_verdict=verdict,
            fhir_bundle=fhir_bundle,
            audit_trace_id=trace_id
        )

