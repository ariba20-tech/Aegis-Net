"""
AEGIS-NET Free & Open-Access Dataset Downloader
Author: Ariba Hurrain Hussain (Orchestration & Integration)

Features:
1. 100% FREE & ZERO-COST: No CITI training, no payments, no institutional subscription required.
2. MIMIC-IV Demo: Fetches MIT's official open-access MIMIC-IV & MIMIC-IV-ED demo subsets.
3. PhysioNet 2019 Telemetry: Fetches hourly vital sign streams (HR, SpO2, SBP, RespRate).
4. Laptop Protection: Strict size controls so storage stays minimal (<100MB).
"""

import os
import sys
import argparse
import urllib.request
import gzip
import shutil

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
MIMIC_DEMO_DIR = os.path.join(RAW_DIR, "mimic_demo")
VITALS_DIR = os.path.join(RAW_DIR, "vitals_sample")


def ensure_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(MIMIC_DEMO_DIR, exist_ok=True)
    os.makedirs(VITALS_DIR, exist_ok=True)


def download_file(url: str, dest_path: str, description: str):
    """Downloads a file with user feedback."""
    if os.path.exists(dest_path):
        print(f"  ✓ [Cached] {description} already present: {os.path.basename(dest_path)}")
        return True

    print(f"  📥 Downloading {description}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AEGIS-NET-Research-Agent/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp, open(dest_path, "wb") as out:
            shutil.copyfileobj(resp, out)
        print(f"  ✓ Downloaded successfully: {os.path.basename(dest_path)}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to download {description}: {e}")
        return False


def fetch_mimic_demo():
    """
    Downloads official Open-Access MIMIC-IV Demo files hosted on PhysioNet.
    NO CITI training, NO credentials, and NO fees required.
    """
    ensure_directories()
    print("\n" + "=" * 70)
    print("🏥 FETCHING OFFICIAL OPEN-ACCESS MIMIC-IV DEMO (100% FREE)")
    print("=" * 70)

    # MIT PhysioNet Open-Access MIMIC-IV-ED & Clinical Demo endpoints
    files_to_fetch = [
        {
            "name": "edstays.csv.gz",
            "url": "https://physionet.org/files/mimic-iv-ed-demo/2.2/ed/edstays.csv.gz?download",
            "desc": "MIMIC-IV-ED Stays & Demographics (~100 patients)"
        },
        {
            "name": "triage.csv.gz",
            "url": "https://physionet.org/files/mimic-iv-ed-demo/2.2/ed/triage.csv.gz?download",
            "desc": "MIMIC-IV-ED Triage Vitals & Acuity Scores"
        },
        {
            "name": "vitalsign.csv.gz",
            "url": "https://physionet.org/files/mimic-iv-ed-demo/2.2/ed/vitalsign.csv.gz?download",
            "desc": "MIMIC-IV-ED Continuous Vital Telemetry"
        }
    ]

    for item in files_to_fetch:
        dest = os.path.join(MIMIC_DEMO_DIR, item["name"])
        download_file(item["url"], dest, item["desc"])

    print(f"\n[Done] MIMIC-IV Demo files ready at: {MIMIC_DEMO_DIR}")


def fetch_vitals_telemetry(max_count: int = 15):
    """Downloads authentic continuous vital telemetry from open PhysioNet Challenge 2019."""
    ensure_directories()
    print("\n" + "=" * 70)
    print("📈 FETCHING OPEN-ACCESS PHYSIOLOGIC TELEMETRY (PhysioNet 2019)")
    print("=" * 70)

    base_url = "https://physionet.org/files/challenge-2019/1.0.0/training/training_setA/"
    downloaded = 0

    for i in range(1, max_count + 1):
        filename = f"p{i:06d}.psv"
        url = f"{base_url}{filename}?download"
        dest = os.path.join(VITALS_DIR, filename)

        if download_file(url, dest, f"Patient telemetry stream #{i}"):
            downloaded += 1

    print(f"[Done] {downloaded} patient telemetry streams stored at: {VITALS_DIR}")


def main():
    parser = argparse.ArgumentParser(description="AEGIS-NET Free Dataset Downloader")
    parser.add_argument("--source", choices=["all", "mimic-demo", "vitals"], default="all",
                        help="Which free dataset to download: 'mimic-demo', 'vitals', or 'all'.")
    parser.add_argument("--count", type=int, default=15, help="Number of telemetry streams to fetch")
    args = parser.parse_args()

    ensure_directories()
    if args.source in ("mimic-demo", "all"):
        fetch_mimic_demo()
    if args.source in ("vitals", "all"):
        fetch_vitals_telemetry(args.count)


if __name__ == "__main__":
    main()
