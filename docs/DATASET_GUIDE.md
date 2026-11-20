# 📚 AEGIS-NET: Free & Zero-Cost Dataset Guide

> [!IMPORTANT]
> **DO NOT PAY FOR CITI PROGRAM OR ANY DATASET.**  
> Individual learner fees on CITI are unnecessary. MIT and the clinical AI research community provide **100% free, open-access datasets** with zero paywalls and zero institutional requirements.

---

## 🏆 1. The Official Open-Access "MIMIC-IV Demo" (Zero CITI, Zero Cost)

MIT and PhysioNet publish the official **MIMIC-IV Clinical Demo** and **MIMIC-IV-ED Demo**. These datasets have the **exact same table structures, schemas, and clinical features** as the full MIMIC database, but are completely open to the public:
- **Zero credentialing required**
- **Zero CITI training required**
- **Zero payment**
- **Size:** Under 10 MB compressed (perfect for a small laptop!)

### What it contains:
* `triage.csv.gz`: Real emergency department triage vitals, temperature, SpO₂, and official triage acuity scores (ESI 1–5).
* `edstays.csv.gz`: Real patient demographic entries, admission and discharge timestamps.
* `vitalsign.csv.gz`: Real serial vital sign measurements during emergency stays.

### How to download it in 1 command:
```bash
python scripts/download_datasets.py --source mimic-demo
```
This automatically fetches the official open-access files directly into `data/raw/mimic_demo/`.

---

## 🔬 2. Free Open Datasets for Teammate Modules

Every member can get production-quality, real-world clinical data completely free:

| Module & Owner | Recommended Free Dataset | Source & Link | Cost / License |
| :--- | :--- | :--- | :--- |
| **Vision Agent**<br>(Sanjoli) | **NIH ChestX-ray14** or **Kaggle Chest X-Ray (Pneumonia)** | [Kaggle Chest X-ray Pneumonia](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) (1.2 GB)<br>or [NIH ChestX-ray14](https://www.kaggle.com/datasets/nih-chest-xrays/data) | **100% Free**<br>Direct 1-click download |
| **EHR / Clinical NLP**<br>(Sanjoli) | **MTSamples (Medical Transcriptions)** | [Kaggle MTSamples](https://www.kaggle.com/datasets/tboyclk/medicaltranscriptions) (5,000 transcribed clinical notes across 40 specialties) | **100% Free**<br>Public Domain / Open |
| **Vitals Agent**<br>(Sanjoli) | **PhysioNet Sepsis Challenge 2019** | Run `python scripts/download_datasets.py --source vitals` | **100% Free**<br>No login needed |
| **Doctor-Critic & Triage**<br>(Ariba & Padmini) | **Pre-packaged AEGIS-NET Benchmark** | Built-in at [data/sample_encounters.json](file:///c:/Users/dell/OneDrive/Pictures/Screenshots/Aegis%20Net/data/sample_encounters.json) + MIMIC-IV-ED Demo | **100% Free**<br>Zero download needed |
| **Multimodal Pairs**<br>(Shared) | **ROCO (Radiology Objects in Context)** | Hugging Face: `datasets.load_dataset("roco")` (80,000 medical image-caption pairs) | **100% Free**<br>Open Source |

---

## 💻 3. Protecting Your Laptop Storage & Hardware

1. **Storage:** Keep raw image downloads below 1–2 GB. Use the sample benchmark `data/sample_encounters.json` for 90% of day-to-day development.
2. **Compute:** Do not train heavy neural networks or VLMs directly on your laptop CPU. Use:
   - **Google Colab** (Free T4 GPU, 15GB VRAM)
   - **Kaggle Notebooks** (Free dual T4 GPUs, 30 hours free per week)
   Export only the final lightweight adapter weights (`.pt` or `.safetensors`, ~50MB) to your local repo.
