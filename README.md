# Cybersecurity SIEM Homelab & Threat Detection Lab

This project showcases a self-built cybersecurity homelab designed to simulate real-world Security Operations Center (SOC) workflows, including log analysis, detection engineering, incident investigation, and automated threat intelligence enrichment.
The goal of this project is to demonstrate how raw system and network telemetry can be transformed into actionable security detections and enriched with external intelligence to support fasster and more effective incident response.

---

## Key Highlights
- Built a multi-source SIEM environment using Splunk
- Developed behavioral detections for real attack techniques
- Simulated attacker activity using Kali Linux (Nmap, brute force, PowerShell)
- Investigated security events using structured SOC workflows
- Implemented automated threat enrichment using VirusTotal + AI (Gemini)
- Correlated logs across multiple sources to identify full attack chains

---

## Lab Architecture
- Splunk Enterprise (Ubuntu Server) - Central SIEM for log ingestion, detection engineering, and investigation
- Windows 11 Endpoint - Primary telemetry source (Security logs, Sysmon, PowerShell, etc.) forwarded via Splunk Universal Forwarder
- Wazuh EDR (Ubuntu Server) - Endpoint detection and response platform providing file integrity monitoring, rule-based threat detection, and host-level visibility
- OPNsense Firewall - Network-level visibility for connection monitoring, traffic validation, and reconnaissance detection
- Kali Linux - Attack simulation platform used to generate realistic adversary activity

---

## Log Sources & Telemetry
This lab leverages multiple high-value log source to provide layered visibility:

Endpoint Logs
- Windows Security Log (authentication, privilege changes)
- Sysmon (process creation, network connections, file activity)
- Task Scheduler Log (persistence mechanisms)
- Windows Defender Log (malware detection
- RDP Logs (remote access tracking)

Network Logs
- Windows Firewall (pfirewall.log for connection level activity)

---
## Detection Engineering
Custom detections were built in Splunk using real telemetry:
- Brute Force Detection
  - Identifies repeated failed login attempts (Event ID 4625)
- Account Compromise Detection
  - Correlates failed logins followed by a successful login
- Suspicious PowerShell Activity
  - Detects encoded commands, remote script execution, and obfuscation
- Persistence Detection
  - Identifies scheduled task creation/modification
- Port Scan Detection
  - Detects reconnaissance behavior using multi-port connection analysis
 
---
# Automated Threat Intelligence (VirusTotal + AI)
This lab includes an automated enrichment pipeline that simulates modern SOC workflows:

Features:
- Extracts file hashes from Sysmon logs
- Queries VirusTotal for reputation data
- Uses AI (Gemini) to generate readable threat summaries
- Sends enriched results back into Splunk

Output:
- Malicious / Suspicious / Harmless scores
- AI-generated investigation summary

---
## SOC Workflow Demonstrated
This project follows a realistic investigation lifecycle:
1. Detection triggered in Splunk
2. Logs analyzed across multiple sources
3. Indicators extracted (IP, domain, hash)
4. Reputation checked via VirusTotal
5. Results enriched and correlated
6. Analyst decision-making supported with context

---
## Key Takeaways
- Built a complete SIEM pipeline from ingestion, detection, investigation, and enrichment
- Demonstrated real-world attacker behaviors and detection strategies
- Correlated endpoint and network telemetry for high-confidence analysis
- Implemented automation to reduce manual triage effort

---
## Future Improvements
- IP and domain-based enrichment (beyond file hashes)
- Detection tuning and alert optimization
- Splunk dashboards and visualization
- Expanded attack simulations



























---
## Overview

The environment consists of multiple virtual machines used to generate and analyze security-relevant activity.

- Ubuntu Server (Splunk Enterprise)
- OPNsense Firewall
- Windows 11 Endpoint (Splunk Universal Forwarder)
- Kali Linux (Attack Simulation)

Logs from the endpoint are ingested into Splunk for centralized analysis.

---

## Objectives

- Build hands-on experience with SIEM tools
- Understand how logs are generated and analyzed
- Simulate attacker behavior in a controlled environment
- Develop investigation and documentation skills

---

## Project Status

This is an active project that will continue to expand with:

- Additional attack simulations
- Detection rule development
- More advanced log analysis
