# Splunk Homelab Setup

This project documents the setup of a basic Splunk homelab used for log collection and analysis.

- Ubuntu Server (Splunk Enterprise)
- Windows 11 Endpoint (log source)
- Splunk Universal Forwarder
- OPNsense firewall for traffic filtering
- Optional: Sysmon for enhanced logging

---

## Ubuntu Server Setup

Start by installing the latest version of Ubuntu Server LTS:

https://ubuntu.com/download/server

Ubuntu Server was chosen because it is lightweight and leaves room for additional services later.


<img width="975" height="746" alt="image" src="https://github.com/user-attachments/assets/0f13cdea-cf23-4a80-a221-53f4d5f098c1" />


<img width="975" height="552" alt="image" src="https://github.com/user-attachments/assets/15443594-4c91-4b8c-b4db-c2718e8f7a1c" />


### During Installation
- Install **OpenSSH** (required for remote management)


<img width="975" height="602" alt="image" src="https://github.com/user-attachments/assets/85777255-0a4a-429d-a798-a6aee9e01619" />


### After Installation
Update the system:


<img width="919" height="344" alt="image" src="https://github.com/user-attachments/assets/b515dd2f-13ca-46aa-82c0-ab7af7b3cdfe" />


```bash
sudo apt update && sudo apt upgrade -y
```

## Install Splunk Enterprise

Now that the Ubuntu server is set up, the next step is installing Splunk Enterprise.

### Create a Splunk Account

Go to the Splunk website and create a free account:

https://www.splunk.com

Splunk offers a free trial of Splunk Enterprise. After the trial period, it automatically converts to the free version, which is sufficient for this homelab.


<img width="975" height="631" alt="image" src="https://github.com/user-attachments/assets/ae0527dd-be4b-437d-a3b3-a9b19fb1cdb6" />


> No payment information required

---

### Download Splunk (Linux .deb)

After creating an account:

1. Navigate to the Splunk Enterprise download page
2. Select the **Linux (.deb)** package
3. Copy the provided **wget link**

---

### Download Splunk on Ubuntu Server

On your ubuntu server, paste the wget command:

```bash
wget -O splunk-10.2.1-abc123-linux-amd64.deb "https://download.splunk.com/products/splunk/releases/10.2.1/linux/splunk-10.2.1-abs123-linux-amd64.deb"
```
---

### Install Splunk

Once the '.deb' file has been downloaded, install it using:

```bash
sudo dpkg -i splunk.deb
```

---

## Start Splunk

After installing Splunk, start the service using:

```bash
sudo /opt/splunk/bin/splunk start --run-as-root
```
## Initial Splunk Setup

During the first startup, you will be prompted to:

- Accept the license and agreement
- Create a username and password

These credentials will be used to access the Splunk web interface.

---

### Enable Splunk on Boot

To ensure Splunk starts automatically when the server reboots, run:

```bash
sudo /opt/splunk/bin/splunk enable boot-start --run-as-root
```

---

## Access the Splunk Web Interface

Once Splunk is running, open a browser on your host machine and navigate to:

http://Ubuntu-Server-IP:8000

Login using the credentials created during setup. If everything is configured correctly, the Splunk dashboard should load without issues.


<img width="975" height="421" alt="image" src="https://github.com/user-attachments/assets/184fca75-c0c9-434b-ae5b-1a688ecf93cb" />


---

## Configure Splunk to Receive Logs

Before logs can be received, the Splunk server must be configured to listen on a port. In the Splunk web interface, navigate to **Settings** in the top right corner, then select **Forwarding & Receiving**. Under the **Receiving Data** section, click **Configure Receiving** and add port 9997. This port will be used by forwarders to send log data to the Splunk server.


<img width="975" height="946" alt="image" src="https://github.com/user-attachments/assets/4e19f2cd-1fa8-46df-9c2e-0bebe6c35a98" />


<img width="975" height="258" alt="image" src="https://github.com/user-attachments/assets/78b99a1b-5471-441d-a11c-2379d10edf99" />

<img width="975" height="138" alt="image" src="https://github.com/user-attachments/assets/67284f20-99d8-4939-952a-008a16a14b81" />


---

## Set Up Windows Endpoint

Now that the Splunk Server is ready to receive data, set up a Windows 11 virtual machine. This system will act as the primary log source and will later be used for testing and simulating activity within the environment.

Once the installation is complete, the Windows machine will be used to:

- Generate Windows Event Logs
- Forward logs to the Splunk Server
- Simulate activity for detection and analysis


<img width="975" height="731" alt="image" src="https://github.com/user-attachments/assets/471c377d-b393-4b64-ab7a-ed09e861463b" />


---

## Install Splunk Universal Forwarder

Download the Splunk Universal Forwarder:

https://www.splunk.com/en_us/download/universal-forwarder.html


<img width="975" height="731" alt="image" src="https://github.com/user-attachments/assets/994df6bb-5d1f-4f3f-9d66-9d4bb913d49e" />


Run the installer as Administrator on the Windows virtual machine. During setup, select the following log sources:

- Application Logs
- Security Logs
- System Logs


<img width="773" height="602" alt="image" src="https://github.com/user-attachments/assets/05a4ee47-c7e8-4ec3-96e5-881036553206" />


Leave the **Deployment Server** field blank. 

When prompted for the receiving indexer, enter: Your-Splunk-Server-IP:9997

<img width="775" height="603" alt="image" src="https://github.com/user-attachments/assets/3bb9b81e-9e51-46eb-9336-57a4685258e5" />


This tells the forwarder where to send log data.

---

## Verify Log Ingestion

After installation completes, the forwarder should begin sending logs automatically. To verify, open the Splunk web interface and naviage to:

- **Apps --> Search & Reporting**


<img width="586" height="536" alt="image" src="https://github.com/user-attachments/assets/ed616ce6-e140-462b-8fad-92f859a71595" />


Run the following query:

```spl
index=*
```


<img width="2547" height="1106" alt="image" src="https://github.com/user-attachments/assets/48064ffd-8b21-4aec-9cfd-fa97c36cba43" />


---

## Troubleshooting

If logs are not appearing in Splunk, verify the forwarder configuration on the Windows virtual machine. 

--- 

### Check inputs.conf

Confirm the file exists at: C:\Program Files\SplunkUniversalForwarder\etc\system\local\inputs.conf

If it does not exist, create it and add the following:
```
[WinEventLog://Application]
disabled = 0
index = main

[WinEventLog://Security]
disabled = 0
index = main

[WinEventLog://System]
disabled = 0
index = main
```
---

### Check outputs.conf

Ensure the forwarder is configured to send data to the Splunk server:
```
[tcpout]
defaultGroup = default-autolb-group

[tcpout:default-autolb-group]
server = Your-Splunk-Server-IP:9997

[tcpout-server://Your-Splunk-Server-IP:9997]
```
---

### Restart Forwarder (Windows Virtual Machine)

```cmd
net stop SplunkForwarder
net start SplunkForwarder
```

---

### Restart Splunk (Ubuntu server)

```bash
sudo /opt/splunk/bin/splunk restart --run-as-root
```

---

## Install Sysmon

Sysmon (System Monitor) provides additional visibility into system activity beyond standard Windows Event Logs.

This includes:

- Process creation
- Network connections
- File creation and modifications

---

### Download Sysmon

Download Sysmon from Microsoft:

https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon

---

### Download Sysmon Configuration

Download the Sysmon configuration file:

https://github.com/SwiftOnSecurity/sysmon-config

The file used in this setup is: sysmonconfig-export.xml

---

### Prepare Sysmon Files

Extract the Sysmon zip file and place the configuration file in the same directory as 'Sysmon64.exe'.

Example location: C:\Users\<Your-User>\Downloads\Sysmon


<img width="975" height="383" alt="image" src="https://github.com/user-attachments/assets/29248631-4ea1-4a02-8c09-58ddbb3402c2" />


---

### Install Sysmon

Open Command Prompt as Administrator and navigate to the Sysmon directory:

```cmd
cd C:\Users\<Your-User>\Downloads\Sysmon
```

Run the installation command:

```cmd
Sysmon64.exe -i sysmonconfig-export.xml
```

## Configure Splunk Forwarder for Sysmon

To ensure Sysmon logs are forwarded to Splunk, update the inputs.conf file.

Path: C:\Program Files\SplunkUniversalForwarder\etc\system\local\inputs.conf

Add the following entry:
```
[WinEventLog://Microsoft-Windows-Sysmon/Operational]
disabled = 0
index = main
```
---

## Update Forwarder Permissions

To reliably collect Sysmon logs, the Splunk Universal Forwarder must have sufficient permissions. Open Command Prompt as Administrator and run:
```cmd
sc config SplunkForwarder obj= LocalSystem
```

## Restart Services

```cmd
net stop SplunkForwarder
net start SplunkForwarder
```

Restart Splunk on Ubuntu Server:

```bash
sudo /opt/splunk/bin/splunk restart --run-as-root
```

---

## Verify Sysmon Logs

To confirm Sysmon logs are being ingested, run the following query in Splunk:

```spl
index=* source=WinEventLog:Microsoft-Windows-Sysmon/Operational
```
---

## OPNsense Firewall Setup

To simulate a realistic network environment and enable traffic monitoring, an OPNsense firewall was deployed as the central gateway for all lab systems. This allows for traffic inspection, filtering, and forwarding logs to Splunk for analysis.

---

### Creating the OPNsense Virtual Machine

Create a new virtual machine dedicated to OPNsense using your virtualization platform.

Download OPNsense from: https://opnsense.org/download/

Configure two network adapter:
- Network Adapter 1 (WAN): NAT
- Network Adapter 2 (LAN): Host-Only

This setup allows:
- WAN --> internet access (via NAT)
- LAN --> internal lab communication (isolated network)

---

### Initial OPNsense setup

Start the VM and proceed through the installer.

During the interface assignment:
- Assign the NAT adapter (em0) as WAN
- Assign the Host-Only adapter (em1) as LAN

Once installation completes, access the console menu and note the assigned IP address for the LAN interface.

If needed, verify your host-only network range on your host machine using ipconfig. Ensure your LAN interface is within the same subnet.

---

### Basic Configuration


<img width="950" height="706" alt="image" src="https://github.com/user-attachments/assets/e6768ce5-dfb2-454d-b670-a91263ccf864" />


Proceed through the setup wizard:
- Leave most settings as default
- Disable "Optimize for Multi-WAN"
- Configure DNS server (1.1.1.1, 8.8.8.8)


<img width="975" height="348" alt="image" src="https://github.com/user-attachments/assets/d284cdc8-a368-425f-99b2-7ce86aab8f4a" />


<img width="975" height="175" alt="image" src="https://github.com/user-attachments/assets/2f5954c8-7c6f-42b3-b1d9-78117eb65138" />


<img width="975" height="488" alt="image" src="https://github.com/user-attachments/assets/2ccb138a-cc53-4ae8-8710-2b035d52067b" />


Set the LAN IP using CIDR notation:
```
OPNsense-IP/24
```
Example:
```
192.168.1.1/24
```

---

### Network Integration

Update all lab machines to use the firewall as their gateway:
- Splunk Server (Ubuntu)
- Windows Endpoint (VM)
- Kali Linux (attacker machine)

Set default gateway to OPNsense LAN IP. This ensures all traffic flows through the firewall for monitoring.

---

### Configuring Syslog Forwarding

To enable ingestion into Splunk, OPNsense was configured to forward logs using syslog.

Navigate to: System --> Logging --> Remote


<img width="975" height="256" alt="image" src="https://github.com/user-attachments/assets/fcb56ddc-cfcd-4a0d-84ed-c3a8835ddb09" />


Add a new remote logging target with the following settings:
- Transport: UDP
- Applications: select all
- Levels: select all
- Facilities: select all
- Hostname: Splunk-Server-IP
- Port: 5514
- Leave RFC5424 unchecked

---

### Splunk Syslog Input Configuration

On the Splunk server, configure a UDP input to receive firewall logs. 

Edit the inputs.conf file
```bash
sudo nano /opt/splunk/etc/system/local/inputs.conf
```

<img width="975" height="113" alt="image" src="https://github.com/user-attachments/assets/05bf52ee-33d8-4bc7-b91a-5ebfd6b8b48e" />


Add:
```
[udp://5514]
connection_host = ip
sourcetype = syslog
index = firewall
disabled = 0
```

### Verifying Log Ingestion

To confirm logs are reaching Splunk:

1. Capture traffic on Splunk server:
```bash
sudo tcpdump -i <interface> port 5514
```

2. In Splunk, run:
```
index=* | stats count by sourcetype
```
Look for syslog. If configured correctly, logs from OPNsense will appear in Splunk.


<img width="2559" height="528" alt="image" src="https://github.com/user-attachments/assets/db1db20b-1ee7-4967-bd10-41496b77e4dc" />


---

### Default Firewall Rules

The default OPNsense LAN rule was used:
- Allow: LAN net --> any

Logging was enabled on this rule to ensure visibility into all traffic during initial testing. Additional rules and segmentation will be implemented later for detection use cases.


