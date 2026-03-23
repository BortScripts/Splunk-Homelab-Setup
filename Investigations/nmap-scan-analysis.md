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

This type of scan is frequently used by attackers to quickly identify open services on a target system.

---

## Log Analysis

Splunk was used to analyze activity generated during the scan.

Example search:
```spl
index=* 192.168.174.132
```

Key observations:

- Multiple inbound connection attempts from a single source IP
- Sequential targeting of a wide range of destination ports
- High volume of traffic within a short time window

These patterns indicate automated scanning behavior rather than normal user activity.

---

## Findings

The activity demonstrates clear indicators of reconnaissance:

- A single source host initiated connections across hundreds of ports
- The scan occurred rapidly, suggesting automated tooling
- The pattern aligns with known Nmap scanning techniques

This behavior would be considered suspicious in a monitored environment and may warrant further investigation.

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






















