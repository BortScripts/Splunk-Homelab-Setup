# Brute Force Detection

## Log Source
- Security Log

## Description
This detection identifies multiple failed login attempts against a user account within a short period of time. This behavior is commonly associated with brute force or password guessing attacks, where an attacker repeatedly attempts different passwords in order to gain access.

## Why it matters
Failed login attempts are one of the earliest indicators of an attack. Attackers often attempt to gain access by guessing passwords, especially against accounts with weak or commonly used credentials. While a single failed login is normal, repeated failures can indicate malicious activity.

## SPL Query

```spl
index=main EventCode=4625
| stats count as failed_attempts by Account_Name host
| where failed_attempts >= 5
| sort - failed_attempts
```

## SOC value
From a SOC perspective, this detection is important for identifying initial access attempts. 

For example,
- Multiple failed login attempts against a single account
- Attempts occurring rapidly or repeatedly
- Activity originating from a single host

Even if the attacker does not successfully log in, this behavior should be investigated because it indicates someone is actively trying to gain access. This detection often serves as the first step in identifying a larger attack sequence.

## Key Event ID
- 4625 (Failed logon)
---

# Successful Login After Failures

## Log Source
- Security Log

## Description
This detection identifies when an account experiences multiple failed login attempts followed by one or more successful logins. This behavior is commonly associated with brute force or credential guessing attacks where an attacker repeatedly attempts passwords until they successfully authenticate.

## Why it matters
Failed login attempts alone indicate that someone is trying to access an account, but they do not confirm that access was gained. When those failed attempts are followed by a successful login, it strongly suggests that valid credentials were eventually obtained. This detection is important because it highlights:
- Potential account compromise
- Weak or guessable passwords
- Successful brute force attacks
- Unauthorized access following repeated failures

## SPL Query

```spl
index=main (EventCode=4625 OR EventCode=4624)
| stats 
    count(eval(EventCode=4625)) as failed_attempts
    count(eval(EventCode=4624)) as successful_logins
    by Account_Name host Logon_Type
| where failed_attempts >= 5 AND successful_logins >= 1
```

## SOC value
From a SOC perspective, this is a high-confidence detection because it links two critical stages of an attack (Multiple failed login attempts (attack activity) and a successful login (potential compromise)).

For example,
- An attacker attempts several incorrect passwords
- Eventually logs in successfully
- Begins executing commands or accessing resources

This sequence provides strong evidence of unauthorized access and should be investigated immediately.

## Key Event IDs
- 4625 (Failed logon)
- 4624 (Successful logon)

---

# Suspicious PowerShell Activity

## Log Source
- Microsoft-Windows-PowerShell/Operational

## Description
This detection identifies suspicious PowerShell activity by analyzing script block logging events (Event ID 4104). It focuses on common attacker techniques such as encoded commands, remote script downloads, and execution of obfuscated code. PowerShell is frequently abused by attackers because it is built into Windows, highly flexible, and capable of executing commands directly in memory without writing files to disk.

## Why it matters
PowerShell is one of the most commonly used tools in modern attacks due to its ability to:
- Execute code without touching disk (fileless attacks)
- Download and execute remote payloads
- Run encoded or obfuscated commands
- Blend in with legitimate administrative activity

With Script Block Logging enabled, this log captures the actual PowerShell commands executed, making it extremely valuable for detection.

## SPL Query

```spl
index=main EventCode=4104
| search ("IEX" OR "Invoke-Expression" OR "DownloadString" OR "Invoke-WebRequest" OR "-enc" OR "EncodedCommand" OR "FromBase64String" OR "Net.WebClient")
| table _time host User Message
```

## SOC value
From a SOC perspective, this is a high-value detection because it reveals attacker behavior directly. 

For example:
- Security log shows successful login
- PowerShell log shows suspicious encoded command
- Sysmon shows process execution

That combination clearly indicates malicious activity

## Key Event ID
- 4104 (Script Block Logging)
