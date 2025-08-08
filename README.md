# SilentOwner
SilentOwner is a stealthy LDAP post-exploitation tool that lets you change the OwnerSID of any AD object—like a user or group—if you have WriteOwner rights. It operates over LDAP using proper SDFlags, enabling silent ownership takeover and privilege escalation without triggering alerts.

## 🔗 Related Tool: [Certipy-ACL](https://github.com/xploitnik/certipy-acl)

If you're looking for `WriteOwner`, `GenericWrite`, or `WriteDACL` paths to begin with, check out [**Certipy-ACL**](https://github.com/xploitnik/certipy-acl) — a stealth LDAP ACL enumerator that highlights effective permissions using SID-based analysis.

Once you identify an object you can take over, use **SilentOwner** to quietly assume ownership and escalate your control — all without a shell.

➡️ Recommended Workflow:
1. Enumerate effective permissions with `certipy-acl`
2. Take ownership with `SilentOwner`
3. (Optional) Inject ACEs or add yourself to groups silently
