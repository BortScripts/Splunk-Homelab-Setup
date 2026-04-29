# VirusTotal Threat Intelligence Automation (v1)

## Overview
This project automates threat intelligence enrichment by integrating Splunk detections, VirusTotal API, and Google Gemini for AI-assisted analysis. When suspicious activity is detected in logs, a Python script is triggered to:
- Extract file hashes (SHA256)
- Query VirusTotal for reputation data
- Use Gemini to generate a readable threat report
- Send enriched results back into Splunk

This simulates a modern SOC workflow where alerts are automatically enriched and summarized to reduce manual analysis.

## Architecture
This project follows a detection-to-enrichment architecture commonly used in modern SOC environments. File activity is first captured at the endpoint using Sysmon (EventCode 15), which generates file hash telemetry. These logs are forwarded to Splunk, where a detection rule identifies potentially suspicious activity and triggers a custom Python script. The script extracts the file hash and queries the VirusTotal API to determine whether the file has been previously associated with malicious behavior. The results are then passed to Google Gemini, which generates a human-readable threat summary to assist with triage. Finally, the enriched data, including both raw threat intelligence and AI-generated analysis, is sent back into Splunk under a custom sourcetype, allowing analysts to investigate and correlate findings with the SIEM.

## Workflow

1. Sysmon logs file activity (EventCode 15 - FileCreateStreamHash)
2. Logs are ingested into Splunk
3. A detection rule identifies suspicious file creation activity
4. Splunk alert triggers the Python script
5. Script extracts the file hash (SHA256)
6. Hash is queried using the VirusTotal API
7. VirusTotal results are sent to Gemini for analysis
8. Gemini generates a readable threat summary
9. Results are formatted and sent back into Splunk
10. Data is indexed under a custom sourcetype

## Script Functionality
- Hash extraction
- Parses alert data from Splunk
- Extracts file hash (SHA256 from Sysmon EventCode 15)

## VirusTotal Lookup
The script queries VirusTotal using the file hash and retrieves:
- Malicious detections
- Suspicious detections
- Harmless classifications

## Output Fields
- file_hash
- malicious_score
- suspicious_score
- harmless_score
- ai_summary


