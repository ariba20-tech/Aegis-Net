# 🏥 AEGIS-NET: Multimodal Multi-Agent Clinical AI System

**AEGIS-NET** is an autonomous, multimodal, multi-agent clinical AI system designed to assist emergency and critical care clinicians by synthesizing diverse diagnostic modalities:
- **Medical Imaging:** Chest X-rays / CT scans via Biomedical VLMs.
- **Unstructured EHR Records:** Clinical notes, medical history, and lab panels via Clinical NLP.
- **Continuous Telemetry:** Time-series physiological waveforms (ECG, SpO₂, blood pressure).

The system integrates these signals using a **LangGraph cyclic orchestrator** and subjects all synthesized findings to a rigorous **Cross-Agent Debate and Doctor-Critic verification layer** before rendering emergency triage decisions and FHIR-compliant diagnostic reports.

---

## 👥 Team Work Distribution & Technical Ownership

| Developer | Role & Technical Module | Core Responsibilities |
| :--- | :--- | :--- |
| **Ariba Hurrain Hussain** | **Orchestration & Integration**<br>`aegis/orchestrator/` | • Design and implement the **LangGraph central orchestrator**<br>• Build the **cyclic execution workflow**<br>• Agent routing, context management & encounter memory<br>• Implement retry mechanisms for low-confidence cases<br>• End-to-end system integration & architecture maintenance |
| **Sanjoli Vaibhav** | **Multimodal Intelligence**<br>`aegis/ingestion/` | • Ingestion & preprocessing pipeline<br>• DICOM medical image processing<br>• **Vision Agent** using Biomedical VLMs<br>• **EHR Agent** using Clinical NLP<br>• **Vitals Agent** using time-series analysis<br>• FHIR conversion & unit normalization |
| **Padmini Rao** | **Evaluation, Safety & Output**<br>`aegis/evaluation/` | • Cross-agent evaluation & debate mechanisms<br>• Confidence scoring & conflict detection<br>• **Doctor-Critic verification layer**<br>• Hallucination, guideline, and clinical plausibility checks<br>• **Red / Yellow / Green triage classification**<br>• Structured clinical reports & FHIR bundle output<br>• Audit logs & traceability |

---

## 🔄 System Architecture & Cyclic Data Flow

```
                                [ Patient Intake ]
                        (DICOM + EHR Notes + Vitals Telemetry)
                                        │
                                        ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │              MODULE 1: Multimodal Intelligence (Sanjoli)              │
    │   • Vision Agent (Biomedical VLM) -> Finding: Airspace Opacity         │
    │   • EHR Agent (Clinical NLP)     -> Finding: Productive Cough & WBC   │
    │   • Vitals Agent (Time-Series)   -> Finding: Hypoxemia (SpO2 89%)      │
    └───────────────────────────────────┬────────────────────────────────────┘
                                        │ Standardized AgentFindingReport
                                        ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │         MODULE 2: LangGraph Central Orchestrator (Ariba)               │
    │   • Encounter Memory & Context Tracking                                │
    │   • Dynamic Routing & Iteration Counter                                │
    └───────────────────────────────────┬────────────────────────────────────┘
                                        │ State passed to Evaluation
                                        ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │           MODULE 3: Validation, Safety & Reporting (Padmini)           │
    │   • Cross-Agent Debate Engine: Surfaces conflicting findings           │
    │   • Doctor-Critic Layer: Checks plausibility & medical guidelines     │
    └───────────────────────────────────┬────────────────────────────────────┘
                                        │
                         [ Critic: Needs Retry? ]
                         /                      \
      Yes (Low Confidence / Conflict)            No (Verified)
                       /                          \
                      ▼                            ▼
         [ Cyclic Retry Loop ]         [ Triage Engine (Red/Yellow/Green) ]
         Returns to Ariba's            [ Structured Clinical Report & FHIR ]
         orchestrator with             [ Audit Logging & Traceability ]
         critic guidance                            │
                      │                             ▼
                      └───► (Iterate)            [ END ]
```

---

## 📂 Repository Directory Layout

```text
Aegis-Net/
├── .gitignore
├── README.md                      # Architecture & Team Ownership Guide
├── requirements.txt               # Lightweight dependency specification
├── run_pipeline.py                # End-to-end runnable demonstration
│
├── aegis/
│   ├── __init__.py
│   │
│   ├── contracts/                 # SHARED: Universal Pydantic data schemas
│   │   ├── __init__.py
│   │   ├── findings.py            # ClinicalFinding, AgentFindingReport
│   │   ├── state.py               # EncounterState (LangGraph TypedDict)
│   │   └── evaluation.py          # DoctorCriticVerdict, TriageLevel, FinalClinicalReport
│   │
│   ├── ingestion/                 # SANJOLI: Multimodal Intelligence
│   │   ├── README.md              # Documentation for Sanjoli & her agent models
│   │   ├── vision_agent.py        # Biomedical VLM agent
│   │   ├── ehr_agent.py           # Clinical NLP agent
│   │   ├── vitals_agent.py        # Time-series telemetry agent
│   │   ├── dicom_processor.py     # DICOM metadata & windowing
│   │   └── fhir_normalizer.py     # Unit normalization & standard LOINC/UCUM
│   │
│   ├── orchestrator/              # ARIBA: Central LangGraph Orchestrator
│   │   ├── README.md              # Architecture of cyclic workflow & memory
│   │   ├── graph.py               # LangGraph StateGraph & conditional edges
│   │   ├── router.py              # Dynamic routing & retry controller
│   │   ├── memory.py              # Longitudinal & encounter context store
│   │   └── nodes.py               # Node execution functions
│   │
│   └── evaluation/                # PADMINI: Validation, Safety & Reporting
│       ├── README.md              # Documentation for Padmini & her critic layers
│       ├── debate_engine.py       # Cross-agent consensus & conflict detection
│       ├── doctor_critic.py       # Plausibility & hallucination guardrail
│       ├── triage.py              # RED / YELLOW / GREEN classification
│       ├── report_generator.py    # Structured report & FHIR bundle builder
│       └── audit_logger.py        # Traceability & audit logging
│
└── tests/
    └── test_pipeline.py           # Unit & integration tests
```

---

## 🚀 Getting Started

### 1. Requirements
Ensure Python 3.10+ is installed:
```bash
pip install -r requirements.txt
```

### 2. Run the End-to-End Cyclic Pipeline
```bash
python run_pipeline.py
```

### 3. Run Unit and Integration Tests
```bash
python -m pytest tests/
```

---

## 🤝 Guidelines for Teammates & AI Coding Agents

When working on your respective module, **do not modify files in other members' directories without coordination**:
- **Sanjoli:** Focus on `aegis/ingestion/`. Implement your VLM, NLP, and signal processing pipelines to return `AgentFindingReport`.
- **Padmini:** Focus on `aegis/evaluation/`. Enhance the prompt engineering, guidelines check, and FHIR export in your critic and report tools.
- **Ariba:** Focus on `aegis/orchestrator/`. Manage graph nodes, cyclic conditions, memory persistence, and system-wide integration.
- **Contracts (`aegis/contracts/`):** Universal schemas agreed upon by the entire team. Any changes must be coordinated.
