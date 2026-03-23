# Nmap Scan Investigation (Splunk Homelab)

This investigation simulates reconnaissance activity using Nmap and analyzes the logs in Splunk. The objective is to identify indicators of port scanning behavior and demonstrate how this activity appears in centralized logs.

---

## Lab Environment

- Splunk Enterprise (Ubuntu Server)
- Windows 11 Endpoint (Splunk Universal Forwarder)
- Kali Linux (Attack Machine)

---

## Data Source 

- Windows 11 Endpoint logs ingested into Splunk

---

## Attack Simulation

A SYN scan was performed using Nmap to simulate reconnaissance activity:

```bash
nmap 192.168.174.130 -sS -p 1-1000
```

- '-sS' performs a TCP SYN scan, commonly used for stealthy reconnaissance
- '-p 1-1000' targets the most common ports


<img width="540" height="170" alt="image" src="https://github.com/user-attachments/assets/191aec70-c7e3-43f1-9155-860c1c939932" />


This type of scan is frequently used by attackers to quickly identify open services on a target system.

---

## Log Analysis

Splunk was used to analyze activity generated during the scan.

<img width="1288" height="690" alt="image" src="https://github.com/user-attachments/assets/0f73083c-438a-4c6d-aefc-f28b53c7a5c0" />


Example search:
```spl
index=* 192.168.174.132
```

Key observations:


<img width="970" height="817" alt="image" src="https://github.com/user-attachments/assets/7067aa44-b626-4245-adc1-74c5cd332cc1" />
*Example of repeated connection attempts targeting SMB (port 445)*

- Multiple inbound connection attempts from a single source IP
- Activity was primarily observed on ports 135, 139 & 445
- These ports are commonly associated with Windows services such as RPC and SMB
- Repeated connection attempts occurred within a short time window

The concentration of activity on these ports suggests targeted probing of common Windows services.

---

## Findings

The activity demonstrates clear indicators of reconnaissance:

- A single source host initiated repeated connections to ports 135, 139, & 445
- These ports are commonly targeted for Windows-based enumeration and exploitation
- The scan occurred rapidly, suggesting automated tooling

This pattern is consistent with targeted reconnaissance against Windows systems.

---

## Response & Remediation

Based on the observed activity, the behavior is consistent with port scanning and would be considered suspicious in a production environment. However, immediate blocking of the source IP may not always be appropriate without additional context.

Recommended actions:

- **Validate the source**
  Determine whether the scanning IP is an internal system, authorized security tool, or unknown external host

- **Assess intent and frequency**
  Repeated or widespread scanning may indicate malicious reconnaissance, while isolated scans could be benign

- **Implement monitoring or alerting**
  Configure alerts in Splunk to detect similar patterns, such as multiple connection attempts across numerous ports

- **Apply network controls if necessary**
  If the activity is confirmed to be unauthorized or malicious, consider blocking the source IP at the firewall or implementing rate-limiting rules

- **Document and escalate if required**
  Escalate the activity according to incident response procedures if it meets defined thresholds

This approach ensures that response actions are based on context rather than automatically blocking potentially legitimate activity.

---

## Conclusion

This lab demonstrates how reconnaissance activity can be identified using centralized logging and basic SIEM analysis. Even simple scans generate detectable patterns that can be used to identify potential threats.






















