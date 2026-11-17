# 📚 AEGIS-NET Dataset & Benchmark Guide

This document outlines the clinical datasets used for training, benchmarking, and evaluating AEGIS-NET across **Vision (Sanjoli)**, **EHR / Clinical NLP (Sanjoli)**, **Time-Series Vitals (Sanjoli)**, and **Doctor-Critic & Triage (Ariba & Padmini)**.

---

## 🎯 1. Instant Test Benchmark (Included in Repo)

You do **not** need to download anything to test the system right now. A curated multimodal benchmark is pre-packaged in:
📁 `data/sample_encounters.json`

It contains 4 complete, realistic clinical cases:
1. **Severe Community-Acquired Bacterial Pneumonia (RED):** Full multimodal alignment (CXR consolidation, leukocytosis on CBC, high fever, severe SpO2 desaturation).
2. **Acute Pulmonary Embolism (RED - Conflict/Debate Case):** Clear CXR with profound tachycardia, hypoxia, and elevated D-dimer. Tests the **Doctor-Critic** and **Debate Engine** when imaging does not show obvious consolidation.
3. **Moderate COPD Exacerbation (YELLOW):** Hyperinflation on CXR, wheezing, mild tachypnea without acute pneumonia.
4. **Mild Viral Upper Respiratory Infection (GREEN):** Stable vitals, outpatient acuity.

---

## 🏆 2. The Golden Multimodal Dataset: MIMIC-IV & MIMIC-CXR

The primary clinical benchmark for academic clinical AI systems is the **MIMIC** ecosystem hosted by MIT and PhysioNet.

### Why MIMIC is the Gold Standard:
- **Patient Linking:** `subject_id` and `stay_id` connect Chest X-rays, clinical notes, continuous vitals, and emergency triage.
- **Real-World Triage:** Contains authentic emergency department acuity scores (ESI 1 through 5, directly mappable to RED, YELLOW, GREEN).

### Step-by-Step Acquisition Guide:
1. **Create an account:** Register at [physionet.org](https://physionet.org/).
2. **Complete CITI Training:**
   - Go to [citiprogram.org](https://about.citiprogram.org/).
   - Complete the free course: **"Data or Specimens Only Research"**.
   - Download the Completion Certificate PDF.
3. **Link Certificate on PhysioNet:**
   - In your PhysioNet profile, submit your CITI certificate number.
   - Approval takes 24–48 hours.
4. **Sign the Data Use Agreement (DUA):**
   - Click "Sign DUA" on [MIMIC-IV-ED](https://physionet.org/content/mimic-iv-ed/) and [MIMIC-CXR](https://physionet.org/content/mimic-cxr/).

---

## 💾 3. Protecting Your Laptop Storage (Crucial Strategy)

Raw MIMIC-CXR images exceed 5 Terabytes. **Do not download the entire dataset.**

### Recommended Lightweight Slices:
1. **`mimic-iv-ed/ed/triage.csv.gz` (~15 MB):** Contains vital signs at triage and official acuity scores.
2. **`mimic-iv-ed/ed/edstays.csv.gz` (~10 MB):** Patient demographic data and admission/discharge times.
3. **`mimic-cxr-reports.tar.gz` (~40 MB):** Radiologist-written diagnostic reports for all X-rays (plain text).
4. **Subset of Images:** Download only the first **500–1,000 paired Chest X-rays** (in JPG format from `mimic-cxr-jpg`), consuming ~300 MB total.

---

## 🌐 4. Instant Open-Access Alternatives (No CITI Wait)

If you or your teammates want to train models immediately without waiting for credential approval:

| Component | Dataset | Link & Access | Size / Format |
| :--- | :--- | :--- | :--- |
| **Vitals (Time-Series)** | **PhysioNet Sepsis Challenge 2019** | [PhysioNet 2019](https://physionet.org/content/challenge-2019/) | Open CSV / PSV files containing hourly HR, SpO2, SBP, RR. |
| **Vision (CXR)** | **NIH ChestX-ray14 / CheXpert Sample** | [Kaggle NIH CXR](https://www.kaggle.com/datasets/nih-chest-xrays/data) | JPEG images with 14 pathology labels. |
| **Clinical NLP (EHR)** | **MTSamples** | [Kaggle MTSamples](https://www.kaggle.com/datasets/tboyclk/medicaltranscriptions) | 5,000 clean transcribed doctor notes across 40 specialties. |

---

## 🛠️ 5. Running the Ingestion Script
To fetch sample open vitals streams directly into your workspace:
```bash
python scripts/download_datasets.py --mode sample --count 20
```

To display full MIMIC credential instructions at any time:
```bash
python scripts/download_datasets.py --mode mimic-guide
```
