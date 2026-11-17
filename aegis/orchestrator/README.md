# Module: Central System Architecture & Orchestration
**Owner:** Ariba Hurrain Hussain  
**Target:** LangGraph Central Orchestrator, Cyclic Execution, Agent Routing & Encounter Memory

---

## 🎯 Purpose & Responsibilities
Ariba owns the central nervous system of AEGIS-NET:
1. **LangGraph StateGraph Core:** Orchestrating the cyclic graph topology across ingestion, multi-agent analysis, evaluation, and reporting.
2. **Cyclic Execution & Retry Mechanisms:** Intelligently rerouting low-confidence cases or conflicting diagnoses back to specialized agents with targeted critic guidance.
3. **Agent Routing & Parallel Execution:** Dynamically routing incoming encounters to appropriate specialized agents (Vision, EHR, Vitals) and aggregating their findings.
4. **Encounter Memory & Context Management:** Tracking past iterations, previous findings, patient history, and state evolution across cyclic passes.
5. **End-to-End System Integration:** Binding Sanjoli's multimodal ingestion agents and Padmini's evaluation/safety layers into a unified clinical AI pipeline.

---

## 🔄 Cyclic Workflow Architecture

```
                    ┌─────────────────────────┐
                    │       intake_node       │ (Initialize Encounter Memory & State)
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       agents_node       │◄─────────────┐
                    │ (Vision + EHR + Vitals) │              │
                    └────────────┬────────────┘              │
                                 │                           │
                                 ▼                           │  (Cyclic Retry Loop)
                    ┌─────────────────────────┐              │  needs_retry == True
                    │     evaluation_node     │              │  iteration <= max_retries
                    │ (Debate + Doctor-Critic)│              │
                    └────────────┬────────────┘              │
                                 │                           │
                                 ▼                           │
                       [ should_retry Router ] ──────────────┘
                                 │
                                 │  needs_retry == False (Verified)
                                 ▼
                    ┌─────────────────────────┐
                    │     reporting_node      │
                    │ (Triage + Final Report) │
                    └────────────┬────────────┘
                                 │
                                 ▼
                              [ END ]
```

---

## 📂 File Architecture
- `graph.py`: StateGraph definition, compilation, and cyclic execution runner.
- `nodes.py`: Node execution logic wrapping specialized agents and evaluation layers.
- `router.py`: Conditional edge routing logic determining retry vs. finalization.
- `memory.py`: Encounter memory store managing patient history and iterative context.
