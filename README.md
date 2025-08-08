# 🛡️ SilentOwner

SilentOwner is a stealthy LDAP post-exploitation tool that lets you **change the OwnerSID** of any Active Directory object — such as a user or group — when your account holds **WriteOwner** permissions.

It operates entirely over LDAP using the correct `SDFlags` control to modify the `nTSecurityDescriptor` attribute. This allows you to **silently assume ownership** of LDAP objects, gain **implicit control**, and prepare **privilege escalation paths** — all without needing a shell or triggering common alerts.

---

## 🔧 Requirements

- Python 3.10+
- `ldap3`
- `impacket`

```bash
pip install ldap3 impacket
```

---

## 🚀 Usage

```bash
python3 SilentOwner.py \
  --dc-ip 10.129.128.69 \
  -u judith.mader@certified.htb \
  -p 'judith09' \
  --domain certified.htb \
  --target-dn 'CN=Management,CN=Users,DC=certified,DC=htb' \
  --new-owner-sid 'S-1-5-21-729746778-2675978091-3820388244-1103'
```

---

## 📄 Example Output

```
🛡️ SilentOwner — Replace LDAP OwnerSID via WriteOwner without touching ACEs
🧬 Built for post-exploitation, stealth privilege escalation, and AD persistence.

🛡️  SilentOwner is live — scanning for target object ownership...

[+] LDAP bind successful.
[DEBUG] Raw sd['OwnerSid']: b''
[!] Owner SID is empty or not set. Proceeding to set a new owner.
[+] Replacing owner with: S-1-5-21-729746778-2675978091-3820388244-1103
[✅] Ownership of CN=Management,CN=Users,DC=certified,DC=htb successfully changed
```

---

## 📸 SilentOwner in action

<img width="2632" height="868" alt="image" src="https://github.com/user-attachments/assets/f12894c2-8a83-4c65-9acc-cf11e1a1a835" />


---

## ⚙️ Arguments

| Flag              | Description                                       |
|-------------------|---------------------------------------------------|
| `--dc-ip`         | IP address of the Domain Controller               |
| `-u, --username`  | LDAP bind username (e.g., `user@domain.local`)    |
| `-p, --password`  | Password for the bind account                     |
| `--domain`        | AD domain name (e.g., `certified.htb`)            |
| `--target-dn`     | Distinguished Name of the object to take over     |
| `--new-owner-sid` | SID to set as the new owner                       |

---

## 🔗 Related Tool: Certipy-ACL

If you're looking for **WriteOwner**, **GenericWrite**, or **WriteDACL** paths to begin with, check out [Certipy-ACL](https://github.com/your-repo/certipy-acl) — a stealth LDAP ACL enumerator that highlights **effective permissions** using **SID-based analysis**.

Once you identify an object you can take over, use **SilentOwner** to quietly assume ownership and escalate your control — all without a shell.

---

## 🧩 Recommended Workflow

1. 🕵️ Enumerate effective permissions using **certipy-acl**
2. 👑 Take ownership with **SilentOwner**
3. 🛠️ *(Optional)* Inject ACEs or silently add yourself to groups

---

## 🛡️ Use Cases

- Escalating privileges in AD environments with delegated rights
- Taking control of groups, service accounts, or user objects
- Preparing post-exploitation paths without triggering logs
- Maintaining stealth persistence via DACL abuse

---

## 💡 Why This Tool Exists

Most privilege escalation tools — like **BloodHound**, **BloodyAD**, or **PowerView** — are built for discovery. They scan the domain, enumerate permissions, and highlight potential abuse paths.

**SilentOwner is different.**

It’s designed for operators who already know **which object they control — specifically via WriteOwner** — and want to **silently take over that object** without scanning, without a shell, and without noise.

This tool picks up *after* discovery — when you're working with SIDs directly and need **surgical control** over LDAP objects for escalation or persistence.

---

## 🧯 Troubleshooting

| Error                        | Explanation                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| ❌ `insufficientAccessRights` | You likely have WriteOwner but forgot the SDFlags=0x01 control.             |
| ❌ `b''` or empty OwnerSID   | Some objects don’t have an explicit owner set — SilentOwner sets it safely. |
| ❌ No effect?                | Double-check your `--new-owner-sid` is valid (e.g., `S-1-5-21-...`)         |

---

## 🛠️ Next Step

Want to take it further?

Once you've taken ownership, you can **inject ACEs** to assign yourself `GenericWrite`, `WriteMember`, or `GenericAll` — all remotely, all silently.

A **companion script** — `inject_ace.py` — is coming soon to expand your control over the target object.

---

> 🧬 Built to empower SIDs — and the people who know how to use them.



