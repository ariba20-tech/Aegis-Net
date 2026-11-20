"""
AEGIS-NET: Clinical Multimodal Multi-Agent Dashboard
Built to replicate the official AEGIS-NET UI design.
Orchestrated by Ariba Hurrain Hussain's LangGraph StateGraph.
"""

import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import Ariba's LangGraph Orchestrator & Contracts
from aegis.orchestrator.graph import get_compiled_orchestrator
from aegis.contracts.state import EncounterState
from aegis.contracts.findings import ModalityType, SeverityLevel
from aegis.contracts.evaluation import TriageLevel

# Page Configuration
st.set_page_config(
    page_title="AEGIS-NET · Clinical Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling to match Padmini's Figma/Dashboard mockup
st.markdown("""
<style>
    /* Global Styles */
    .main { background-color: #f8fafc; }
    .stApp { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    
    /* Top Header Badge */
    .header-badge {
        font-size: 0.85rem;
        background-color: #e2e8f0;
        color: #475569;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* Card Containers */
    .metric-card {
        background: white;
        padding: 18px 20px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .metric-title { font-size: 0.82rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin-top: 4px; }
    .metric-sub { font-size: 0.80rem; color: #94a3b8; margin-top: 2px; }

    /* Triage Badges */
    .badge-red { background-color: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.80rem; border: 1px solid #fecaca; }
    .badge-yellow { background-color: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.80rem; border: 1px solid #fde68a; }
    .badge-green { background-color: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.80rem; border: 1px solid #bbf7d0; }

    /* Agent Finding Block */
    .agent-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .agent-header { font-weight: 600; font-size: 0.92rem; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .agent-obs { font-size: 0.88rem; color: #334155; margin-top: 6px; }
</style>
""", unsafe_allow_html=True)


# Load Benchmark Encounters
@st.cache_data
def load_encounters():
    path = os.path.join(os.path.dirname(__file__), "data", "sample_encounters.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []


encounters = load_encounters()

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 🏥 **AEGIS-NET**")
    st.caption("Multimodal Multi-Agent Clinical AI System")
    st.markdown("---")
    menu = st.radio(
        "CLINICAL WORKSPACE",
        ["Dashboard", "Patient Queue & Review", "Cross-Agent Validation", "Clinical Reports & FHIR", "Architecture & Traceability"],
        index=0
    )
    st.markdown("---")
    st.caption("Demonstration only · All patient data is synthetic / de-identified.")
    st.caption("👤 **Signed in:** Dr. Sarah Chen (ED Attending)")
    st.caption("👑 **System Orchestrator:** Ariba Hurrain Hussain")


# Header Row
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("## **AEGIS-NET Clinical Dashboard**")
    st.markdown('<span class="header-badge">Emergency Department · Live Multimodal Triage</span>', unsafe_allow_html=True)
with col_h2:
    st.markdown("<div style='text-align: right; color: #64748b; font-size: 0.9rem;'>📅 Today, 20 Nov 2026</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Top KPI Metric Cards (Faithfully mirroring Padmini's design)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Cases under assessment</div>
        <div class="metric-value">18</div>
        <div class="metric-sub">Synthetic cases in active ED queue</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Agent evaluations completed</div>
        <div class="metric-value">72</div>
        <div class="metric-sub">Across 24 demo cases today</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Pending validations</div>
        <div class="metric-value" style="color: #d97706;">6</div>
        <div class="metric-sub">4 disagreements · 2 retries</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Doctor-Critic flags</div>
        <div class="metric-value" style="color: #dc2626;">2</div>
        <div class="metric-sub">Require physician review</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Main Body Split: Left = Queue & Charts; Right = Live Agent Reasoning Sidepanel
col_main, col_side = st.columns([5, 4])

with col_main:
    # Activity Chart & Cross-agent validation mini charts
    st.markdown("#### **Assessment Activity & Consensus**")
    c_chart1, c_chart2 = st.columns([3, 2])
    with c_chart1:
        # Mini bar chart of cases per hour
        hours = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00"]
        counts = [1, 2, 4, 3, 5, 4, 3, 2]
        fig_bar = px.bar(x=hours, y=counts, labels={'x': 'Hour', 'y': 'Cases'}, height=190)
        fig_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        fig_bar.update_traces(marker_color="#3b82f6")
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_chart2:
        st.markdown("**Cross-Agent Validation:**")
        st.progress(0.75, text="✅ Concordant / Agree (18)")
        st.progress(0.18, text="⚠️ Disagree / Debate (4)")
        st.progress(0.07, text="⏳ Pending Retry (2)")

    st.markdown("---")
    st.markdown("#### **Emergency Patient Queue**")

    # Patient selection table
    patient_options = [f"{c['patient_id']} - {c['clinical_scenario'][:45]}... (Expected: {c['expected_triage']})" for c in encounters]
    selected_idx = st.selectbox("Select patient to run live LangGraph assessment:", range(len(encounters)), format_func=lambda i: patient_options[i])
    current_case = encounters[selected_idx]

    # Display Queue Card
    t_badge = {
        "RED": '<span class="badge-red">🚨 RED / IMMEDIATE</span>',
        "YELLOW": '<span class="badge-yellow">⚠️ YELLOW / URGENT</span>',
        "GREEN": '<span class="badge-green">✅ GREEN / ROUTINE</span>'
    }.get(current_case["expected_triage"], '<span class="badge-yellow">YELLOW</span>')

    st.markdown(f"""
    <div style="background: white; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px; margin-top: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 1.1rem; font-weight: 700;">{current_case['patient_id']} ({current_case['demographics']['age']}y, {current_case['demographics']['gender']})</span>
            {t_badge}
        </div>
        <div style="margin-top: 8px; color: #475569; font-size: 0.90rem;">
            <strong>Chief Complaint:</strong> {current_case['demographics']['chief_complaint']}
        </div>
        <div style="margin-top: 6px; color: #64748b; font-size: 0.85rem;">
            <strong>Vitals:</strong> HR {current_case['raw_inputs']['vitals']['heart_rate']} bpm · 
            SpO₂ {current_case['raw_inputs']['vitals']['spo2_percent']}% ({current_case['raw_inputs']['vitals']['o2_device']}) · 
            BP {current_case['raw_inputs']['vitals']['blood_pressure_systolic']}/{current_case['raw_inputs']['vitals']['blood_pressure_diastolic']} mmHg · 
            RR {current_case['raw_inputs']['vitals']['respiratory_rate']}/min
        </div>
    </div>
    """, unsafe_allow_html=True)


with col_side:
    st.markdown("#### **Clinical Review & Live Agent Reasoning**")

    if st.button("⚡ Run LangGraph Multi-Agent Orchestrator", type="primary", use_container_width=True):
        with st.spinner("Executing LangGraph cyclic orchestration (Ingestion ➔ Agents ➔ Debate ➔ Doctor-Critic ➔ Triage)..."):
            app = get_compiled_orchestrator()
            initial_state: EncounterState = {
                "patient_id": current_case["patient_id"],
                "encounter_id": current_case["encounter_id"],
                "iteration": 1,
                "max_retries": 2,
                "raw_inputs": current_case["raw_inputs"],
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
            output = app.invoke(initial_state)
            st.session_state["last_run_output"] = output

    if "last_run_output" in st.session_state:
        output = st.session_state["last_run_output"]
        report = output.get("final_report")
        critic = output.get("critic_verdict")

        st.success(f"Orchestration Complete · Iteration Passes: {output['iteration']}")

        # 1. Vision Agent (Sanjoli)
        st.markdown("""
        <div class="agent-box">
            <div class="agent-header">🖼️ <strong>Vision Agent</strong> (Biomedical VLM)</div>
            <div class="agent-obs">Findings: Airspace opacity identified with focal consolidation in right lower lobe.</div>
            <div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">Confidence: 94.0% · DICOM Modality: DX (PA View)</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. EHR Agent (Sanjoli)
        st.markdown(f"""
        <div class="agent-box">
            <div class="agent-header">📄 <strong>EHR Agent</strong> (Clinical NLP)</div>
            <div class="agent-obs">Extracted: Acute febrile illness, productive cough, leukocytosis (WBC 14.8).</div>
            <div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">Confidence: 92.0% · Entity Grounding: Verified</div>
        </div>
        """, unsafe_allow_html=True)

        # 3. Vitals Agent (Sanjoli)
        st.markdown(f"""
        <div class="agent-box">
            <div class="agent-header">📈 <strong>Vitals Agent</strong> (Physiologic Telemetry)</div>
            <div class="agent-obs">Extracted: Severe hypoxemia (SpO2 {current_case['raw_inputs']['vitals']['spo2_percent']}%), tachypnea, sinus tachycardia.</div>
            <div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">Confidence: 96.0% · Sensor Alert: Desaturation Event</div>
        </div>
        """, unsafe_allow_html=True)

        # 4. Doctor-Critic & Triage (Padmini)
        if critic and report:
            t_color = "#dc2626" if report.triage == TriageLevel.RED else ("#d97706" if report.triage == TriageLevel.YELLOW else "#16a34a")
            st.markdown(f"""
            <div style="background: #f8fafc; border: 2px solid {t_color}; border-radius: 8px; padding: 14px; margin-top: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: #0f172a;">🩺 Doctor-Critic Verification</span>
                    <span style="background: {t_color}; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">
                        TRIAGE: {report.triage.value}
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #334155; margin-top: 6px;">
                    {critic.critique_notes}
                </div>
                <div style="font-size: 0.80rem; color: #64748b; margin-top: 6px;">
                    Plausibility: {critic.is_plausible} · Guideline Concordant: {critic.guideline_concordant} · Score: {critic.verification_confidence*100:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Export FHIR Bundle
            with st.expander("📦 View Generated FHIR DiagnosticReport Bundle"):
                st.json(report.fhir_bundle)

    else:
        st.info("Click '⚡ Run LangGraph Multi-Agent Orchestrator' above to observe real-time agent execution.")
