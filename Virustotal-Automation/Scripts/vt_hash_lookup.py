#!/usr/bin/env python3

from dotenv import load_dotenv
from google import genai
import os
import sys
import json
import requests
from datetime import datetime
import re
import gzip
import traceback
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
REPORT_DIR = BASE_DIR / "reports"
DEBUG_LOG = BASE_DIR / "logs" / "triage_debug_steps.log"

# Splunk HEC endpoint
SPLUNK_HEC_URL = "https://localhost:8088/services/collector"


def debug(message):
    DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(DEBUG_LOG, "a") as f:
        f.write(f"{datetime.now()} | {message}\n")


load_dotenv(ENV_PATH)

VT_API_KEY = os.getenv("VT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SPLUNK_HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN")


def get_hash_from_input():
    debug("Entered get_hash_from_input()")
    debug(f"sys.argv = {json.dumps(sys.argv)}")

    for arg in sys.argv[1:]:
        match = re.search(r"\b[A-Fa-f0-9]{64}\b", arg)
        if match:
            file_hash = match.group(0)
            debug(f"Found hash in argv: {file_hash}")
            return file_hash

    for arg in sys.argv[1:]:
        if arg.endswith(".csv.gz"):
            debug(f"Found CSV.GZ arg: {arg}")

            try:
                with gzip.open(arg, "rt") as f:
                    content = f.read()

                match = re.search(r"SHA256=([A-Fa-f0-9]{64})", content)
                if match:
                    file_hash = match.group(1)
                    debug(f"Found hash from SHA256 pattern in CSV: {file_hash}")
                    return file_hash

                match = re.search(r"\b[A-Fa-f0-9]{64}\b", content)
                if match:
                    file_hash = match.group(0)
                    debug(f"Found generic SHA256 hash in CSV: {file_hash}")
                    return file_hash

            except Exception:
                debug("Exception while reading CSV.GZ")
                debug(traceback.format_exc())

    debug("No hash found")
    return None


def get_vt_file_report(file_hash):
    debug("Entered get_vt_file_report()")

    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VT_API_KEY}

    response = requests.get(url, headers=headers, timeout=30)
    debug(f"VirusTotal HTTP status: {response.status_code}")

    if response.status_code == 404:
        return {
            "found": False,
            "message": "Hash was not found in VirusTotal.",
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0,
            "undetected": 0,
        }

    if response.status_code != 200:
        return {
            "found": False,
            "message": f"VirusTotal error: {response.status_code}",
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0,
            "undetected": 0,
        }

    data = response.json()
    attributes = data.get("data", {}).get("attributes", {})
    stats = attributes.get("last_analysis_stats", {})

    return {
        "found": True,
        "sha256": attributes.get("sha256"),
        "meaningful_name": attributes.get("meaningful_name"),
        "type_description": attributes.get("type_description"),
        "reputation": attributes.get("reputation"),
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
        "undetected": stats.get("undetected", 0),
        "last_analysis_stats": stats,
    }


def calculate_severity(vt_result):
    malicious = vt_result.get("malicious", 0)
    suspicious = vt_result.get("suspicious", 0)

    if not vt_result.get("found"):
        return "Unknown"
    elif malicious >= 10:
        return "Critical"
    elif malicious >= 5:
        return "High"
    elif malicious >= 1:
        return "Medium"
    elif suspicious >= 1:
        return "Low"
    else:
        return "Informational"


def generate_gemini_report(file_hash, vt_result, severity):
    debug("Entered generate_gemini_report()")

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
You are writing a SOC analyst triage report.

Artifact Type: File Hash
Artifact Value: {file_hash}

VirusTotal Result:
{json.dumps(vt_result, indent=2)}

Calculated Severity: {severity}

Write the report in this format:

Title:
Summary:
Severity:
Evidence:
VirusTotal Findings:
Risk Explanation:
Recommended Remediation:
Next Steps:

Keep it professional, clear, and beginner-friendly.
Do not invent details that are not present in the data.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    debug("Gemini response received")
    return response.text


def save_report(file_hash, report_text, vt_result, severity):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = REPORT_DIR / f"hash_report_{timestamp}_{file_hash[:8]}.md"

    with open(filename, "w") as f:
        f.write("# AI-Assisted SOC Triage Report\n\n")
        f.write(report_text)
        f.write("\n\n---\n\n")
        f.write("## Raw Data\n\n")
        f.write("```json\n")
        f.write(json.dumps({
            "artifact_type": "hash",
            "artifact_value": file_hash,
            "severity": severity,
            "virustotal": vt_result,
        }, indent=2))
        f.write("\n```")

    return str(filename)


def send_to_splunk(report_text, vt_result, severity, file_hash, report_path):
    headers = {
        "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}"
    }

    splunk_event = {
        "sourcetype": "vt:gemini:report",
        "index": "main",
        "event": {
            "event_type": "vt_gemini_report",
            "artifact_type": "hash",
            "artifact_value": file_hash,
            "severity": severity,
            "report_path": report_path,
            "report": report_text,
            "vt_found": vt_result.get("found"),
            "vt_malicious": vt_result.get("malicious", 0),
            "vt_suspicious": vt_result.get("suspicious", 0),
            "vt_harmless": vt_result.get("harmless", 0),
            "vt_undetected": vt_result.get("undetected", 0),
            "vt_reputation": vt_result.get("reputation"),
            "vt_meaningful_name": vt_result.get("meaningful_name"),
            "vt_type_description": vt_result.get("type_description"),
        },
    }

    response = requests.post(
        SPLUNK_HEC_URL,
        headers=headers,
        json=splunk_event,
        timeout=30,
        verify=False,  # Lab-only setting for local Splunk HEC
    )

    debug(f"Splunk HEC status: {response.status_code}")
    debug(f"Splunk HEC response: {response.text[:300]}")


def main():
    debug("===== NEW TRIAGE RUN STARTED =====")

    if not VT_API_KEY:
        debug("VT_API_KEY missing")
        sys.exit(1)

    if not GEMINI_API_KEY:
        debug("GEMINI_API_KEY missing")
        sys.exit(1)

    if not SPLUNK_HEC_TOKEN:
        debug("SPLUNK_HEC_TOKEN missing")
        sys.exit(1)

    file_hash = get_hash_from_input()

    if not file_hash:
        debug("No SHA256 hash found")
        sys.exit(1)

    debug(f"Hash found: {file_hash}")

    vt_result = get_vt_file_report(file_hash)
    severity = calculate_severity(vt_result)

    report_text = generate_gemini_report(file_hash, vt_result, severity)
    report_path = save_report(file_hash, report_text, vt_result, severity)

    send_to_splunk(report_text, vt_result, severity, file_hash, report_path)

    debug("===== TRIAGE RUN COMPLETED SUCCESSFULLY =====")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        debug("FATAL ERROR:")
        debug(traceback.format_exc())
        sys.exit(1)
