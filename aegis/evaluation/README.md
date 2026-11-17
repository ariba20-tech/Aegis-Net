# Module: Validation, Safety & Clinical Reporting
**Owner:** Padmini Rao  
**Target:** Cross-Agent Debate, Doctor-Critic Verification, Triage, and Reporting

---

## 🎯 Purpose & Responsibilities
This module acts as the clinical safety and evaluation authority of AEGIS-NET:
1. **Cross-Agent Debate & Conflict Detection:** Analyzes findings across Vision, EHR, and Vitals to identify discrepancies (e.g. imaging shows clear lungs, but vitals show severe hypoxia).
2. **Doctor-Critic Verification Layer:** Evaluates whether synthesized diagnoses are clinically plausible, evidence-grounded, and free from hallucinations or guideline deviations.
3. **Triggering Cyclic Retries:** If confidence is below threshold or unresolved contradictions exist, issues `needs_retry=True` with actionable `retry_guidance` back to Ariba's orchestrator.
4. **Triage Classification:** Categorizes the patient into **GREEN**, **YELLOW**, or **RED** acuity.
5. **Structured Clinical Reporting & FHIR Export:** Produces clear summaries for attending physicians and outputs compliant FHIR bundles.
6. **Audit Logs & Traceability:** Logs every reasoning step, critic decision, and retry trigger for medical governance.

---

## 🔌 Integration Contract with Ariba's Orchestrator
Padmini's module accepts the accumulated `agent_reports` and `accumulated_findings` from `EncounterState`, and produces:
- `List[ConflictItem]` (from `debate_engine.py`)
- `DoctorCriticVerdict` (from `doctor_critic.py`)
- `TriageLevel` (from `triage.py`)
- `FinalClinicalReport` (from `report_generator.py`)

### Critic Verdict Example:
```python
from aegis.contracts.evaluation import DoctorCriticVerdict

verdict = DoctorCriticVerdict(
    is_plausible=True,
    hallucination_detected=False,
    guideline_concordant=True,
    verification_confidence=0.91,
    critique_notes="Findings across CXR and CBC are concordant with community-acquired pneumonia.",
    needs_retry=False,
    retry_guidance=None
)
```

---

## 📂 File Architecture
- `debate_engine.py`: Inter-modality consensus scoring and cross-agent debate.
- `doctor_critic.py`: Safety verification and hallucination detection.
- `triage.py`: Deterministic and learned clinical triage classification (RED / YELLOW / GREEN).
- `report_generator.py`: Attending physician report and FHIR bundle builder.
- `audit_logger.py`: Encounter traceability and structured audit logging.
