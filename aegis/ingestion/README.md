# Module: Multimodal Intelligence & Data Ingestion
**Owner:** Sanjoli Vaibhav  
**Target:** Biomedical VLMs, Clinical NLP, Time-Series Analysis & FHIR Normalization

---

## 🎯 Purpose & Responsibilities
This module is responsible for ingesting multimodal patient data and extracting structured clinical observations:
1. **Medical Imaging (DICOM):** Preprocessing chest X-rays, CT scans, and applying Biomedical Vision-Language Models (e.g., Med-PaLM M, BioViL, or LLaVA-Med).
2. **Clinical EHR Notes & Labs:** Processing unstructured clinician notes, discharge summaries, and lab panels with Clinical NLP (e.g., ClinicalBERT, GatorTron, BioClinicalBERT).
3. **Continuous Vitals:** Analyzing time-series signals (ECG waveforms, SpO₂ desaturations, blood pressure trends, heart rate variability).
4. **Unit Normalization & FHIR:** Converting raw incoming data into standardized units and FHIR observation formats.

---

## 🔌 Integration Contract with Ariba's Orchestrator
Every specialized agent developed in this module must return an `AgentFindingReport` containing one or more `ClinicalFinding` objects defined in `aegis.contracts.findings`.

### Expected Output Example:
```python
from aegis.contracts.findings import AgentFindingReport, ClinicalFinding, ModalityType, SeverityLevel

report = AgentFindingReport(
    agent_name="VisionAgent",
    modality=ModalityType.VISION,
    overall_confidence=0.92,
    findings=[
        ClinicalFinding(
            finding_id="F-VIS-001",
            modality=ModalityType.VISION,
            concept_name="Right Lower Lobe Consolidation",
            observation="Patchy opacity in the right lower lobe suggestive of bacterial pneumonia.",
            evidence_or_roi="bbox:[140, 210, 310, 420]",
            confidence=0.92,
            severity=SeverityLevel.MODERATE,
            metadata={"dicom_modality": "DX", "slice": "PA View"}
        )
    ],
    raw_summary="Probable right lower lobe pneumonia with no pneumothorax."
)
```

---

## 📂 File Architecture
- `dicom_processor.py`: Ingestion, windowing, and standardization of DICOM images.
- `vision_agent.py`: Biomedical VLM inference for medical image interpretation.
- `ehr_agent.py`: Clinical NLP pipeline for extracting entities, relations, and negation.
- `vitals_agent.py`: Time-series anomaly detection and signal processing for ECG / SpO₂.
- `fhir_normalizer.py`: Units normalization (e.g. mg/dL vs mmol/L) and FHIR observation alignment.

