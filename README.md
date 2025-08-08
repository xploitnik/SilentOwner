# 🛡️ SilentOwner

**SilentOwner** is a stealthy LDAP post-exploitation tool that lets you change the `OwnerSID` of any Active Directory object — such as a user or group — when your account holds **`WriteOwner`** permissions.

It operates entirely over LDAP using the correct `SDFlags` control to modify the `nTSecurityDescriptor` attribute. This allows you to silently assume ownership of LDAP objects, gain implicit control, and prepare privilege escalation paths — all without needing a shell or triggering common alerts.

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
python3 replace_owner.py \
  --dc-ip 10.129.128.69 \
  -u judith.mader@certified.htb \
  -p 'judith09' \
  --domain certified.htb \
  --target-dn 'CN=Management,CN=Users,DC=certified,DC=htb' \
  --new-owner-sid 'S-1-5-21-729746778-2675978091-3820388244-1103'
```

---

## 🎯 What This Tool Does

- 🧠 Replaces the `OwnerSID` of any LDAP object you have **`WriteOwner`** rights over
- 🔐 Grants you implicit `WriteDACL` and `ReadControl` (even if ACEs don’t say so)
- 📡 Works entirely over LDAP — no shell required
- 🔕 Does not generate group change logs or certificate logs

---

## 🔗 Related Tool: [Certipy-ACL](https://github.com/xploitnik/certipy-acl)

If you're looking for `WriteOwner`, `GenericWrite`, or `WriteDACL` paths to begin with, check out [**Certipy-ACL**](https://github.com/xploitnik/certipy-acl) — a stealth LDAP ACL enumerator that highlights effective permissions using SID-based analysis.

Once you identify an object you can take over, use **SilentOwner** to quietly assume ownership and escalate your control — all without a shell.

---

## 🧩 Recommended Workflow

1. 🕵️ Enumerate effective permissions using `certipy-acl`
2. 👑 Take ownership with `SilentOwner`
3. 🛠️ (Optional) Inject ACEs or silently add yourself to groups

---

## 🛡️ Use Cases

- Escalating privileges in AD environments with delegated rights
- Taking control of groups, service accounts, or user objects
- Preparing post-exploitation paths without triggering logs
- Maintaining stealth persistence via DACL abuse

---

> _Built to empower SIDs — and the people who know how to use them._

