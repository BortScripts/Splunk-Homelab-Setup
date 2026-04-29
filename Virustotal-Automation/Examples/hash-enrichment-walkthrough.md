## Overview
This example demonstrates end-to-end enrichment of a file hash using Sysmon, Splunk, VirusTotal, and Google Gemini.

## Activity Performed
The Wireshark installer was downloaded to generate file activity on the endpoint.

## Detection
- Sysmon EventCode 15 (FileCreateStreamHash) captured the file hash
- Logs were forwarded into Splunk
- A detection rule identified the event and triggered the enrichment script

## Enrichment Process
Once the alert triggered:
- The script extracted the SHA256 hash from the event
- The hash was queried using VirusTotal
- VirusTotal results were sent to Gemini
- Gemini generated a SOC-style triage report
- The enriched result was written back into Splunk


```json
{
  "event_type": "vt_gemini_report",
  "artifact_type": "hash",
  "artifact_value": "102017D8E99A75B57895CD2144E6A61DC335A8FF14C7A25BD83A55F8EA9AD77B",
  "severity": "Informational",
  "report_path": "/reports/hash_report_20260428_225337_102017D8.md",
  "vt_found": true,
  "vt_malicious": 0,
  "vt_suspicious": 0,
  "vt_harmless": 0,
  "vt_undetected": 64,
  "vt_reputation": 1,
  "vt_meaningful_name": "Wireshark-4.6.4-x64.exe",
  "vt_type_description": "Win32 EXE",
  "report": {
    "title": "SOC Triage Report - File Hash Analysis (Informational)",
    "summary": "The file hash corresponds to Wireshark-4.6.4-x64.exe, a legitimate network protocol analyzer. VirusTotal results show zero detections for malicious or suspicious activity across all security vendors.",
    "severity": "Informational",
    "evidence": {
      "artifact_type": "File Hash (SHA256)",
      "artifact_value": "102017D8E99A75B57895CD2144E6A61DC335A8FF14C7A25BD83A55F8EA9AD77B"
    },
    "virustotal_findings": {
      "hash_found": true,
      "meaningful_name": "Wireshark-4.6.4-x64.exe",
      "type_description": "Win32 EXE",
      "reputation": 1,
      "detection_ratio": "0/64",
      "last_analysis_stats": {
        "malicious": 0,
        "suspicious": 0,
        "undetected": 64
      }
    },
    "risk_explanation": "The file hash is identified as a known, legitimate installer for Wireshark. The absence of malicious or suspicious detections strongly indicates that this file is not a threat.",
    "recommended_remediation": "No direct remediation is required if the file is expected and authorized.",
    "next_steps": [
      "Verify whether Wireshark is expected and authorized on the system.",
      "Close the alert if the file is legitimate and expected.",
      "Investigate the installation if Wireshark is not approved software."
    ]
  }
}
```

## Why This Matters
This demonstrates how raw endpoint telemetry can be automatically enriched with threat intelligence and AI-generated analysis, reducing manual investigation time for SOC analysts.
