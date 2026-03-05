# My Homelab

##  Overview
This repository documents my personal, isolated homelab environment built for practicing penetration testing, vulnerability assessment, and understanding web application security flaws. The infrastructure is designed to simulate a real-world, containerized corporate environment, complete with active defenses and zero-trust networking.

##  Infrastructure & Network Architecture
The environment is hosted on an **Ubuntu Linux** server (`lab-01`).
**Zero-Trust Overlay Network:** Access to the lab is strictly routed through **Tailscale** (WireGuard-based mesh network), making the internal services inaccessible from the public internet.
**Containerization:** All services run in highly isolated **Docker** containers (subnets `172.17.x.x`), protecting the host kernel.

##  Security Perimeter (Defense in Depth)
To study both offensive and defensive mechanics, the lab is heavily monitored and secured.
**L4 Firewall:** **UFW** (Uncomplicated Firewall) enforces strict port-level access control.
IPS (Intrusion Prevention System):** **CrowdSec** actively parses `auth.log`, `syslog`, and reverse proxy logs in real-time to ban malicious IPs . My Kali Linux attacker machine is explicitly whitelisted to allow continuous testing
**DNS Sinkhole:** **AdGuard Home** manages DNS resolution, blocking trackers and malware domains at the network level.
##  Active Service Inventory
The Docker engine hosts multiple production and vulnerable services.
**Nginx Proxy Manager:** Manages reverse proxying and SSL routing.
**Nextcloud & MariaDB:** A self-hosted cloud platform used to test brute-force protections (Rate Limiting/Throttling).
**DVWA (Damn Vulnerable Web App):** The primary "Cyber Range" used for practicing web exploitation
**Management & Monitoring:** Portainer, Homarr, Uptime Kuma, and Dashdot.
##  Vulnerabilities Researched & Exploited
This ledger details the operations conducted against the lab's services.

### 1. Brute Force & Rate Limiting Evasion (Nextcloud)
**Operation:** Developed a custom Python script utilizing the `BeautifulSoup` library for web scraping 
**Execution:** Successfully performed dynamic extraction and submission of CSRF tokens to bypass initial login form protections .
**Result:** Defended successfully by the system. [cite_start]The platform absorbed the attack via server-side throttling, demonstrating effective defensive mechanism 

### 2. Manual SQL Injection (DVWA - Multiple Levels)
**Low Level:** Exploited lack of sanitization via string concatenation (`user_id = '$id'`) using the tautology payload `1' OR '1'='1` 
**Medium Level:** Bypassed client-side restrictions (Dropdown menu) using DOM Manipulation via browser Developer Tools, proving frontend validation is insecure 
**High Level:** Defeated session-based input routing and the `LIMIT 1` SQL constraint by utilizing SQL Commenting (`#` or `-- `) to force the database to ignore the limit clause.
### 3. Automated Blind SQL Injection & Data Exfiltration
Utilized **sqlmap** to automate Boolean-based Blind SQL Injection
Injected payloads directly into the Session Cookie (`PHPSESSID`) to bypass GET/POST parameter restrictions.
Successfully enumerated databases, tables, and columns, ultimately extracting and cracking MD5 password hashes.

## 📝 Disclaimer
All activities documented in this repository were performed on a locally hosted, private network owned by me. This environment was strictly built for educational purposes, defensive analysis, and ethical hacking practice.
