#!/usr/bin/env python3
"""Connection verification utility for Oktopost API."""

import base64
import json
import os
import sys
import urllib.request
import urllib.error

CLAUDE_MAIN_CONFIG = os.path.expanduser("~/.claude.json")            # primary: MCP servers live here
CLAUDE_LEGACY_CONFIG = os.path.expanduser("~/.claude/settings.json")  # legacy location
REGIONS = {"us": "https://api.oktopost.com", "eu": "https://api.eu.oktopost.com"}


def _from_claude_config(path):
    """Extract oktopost MCP env dict from a Claude Code config file, or None."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            cfg = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    servers = cfg.get("mcpServers", {})
    mcp = servers.get("oktopost") or servers.get("oktopost-mcp") or {}
    env = mcp.get("env") or {}
    if not env.get("OKTOPOST_API_KEY"):
        return None
    return env


def get_credentials():
    # 1. env vars (highest precedence -- used by CI and explicit fallback invocations)
    region = os.environ.get("OKTOPOST_ACCOUNT_REGION")
    account_id = os.environ.get("OKTOPOST_ACCOUNT_ID")
    api_key = os.environ.get("OKTOPOST_API_KEY")
    if account_id and api_key:
        return region or "us", account_id, api_key
    # 2. ~/.claude.json (where `claude mcp add` actually writes)
    env = _from_claude_config(CLAUDE_MAIN_CONFIG)
    if env is None:
        # 3. legacy ~/.claude/settings.json fallback
        env = _from_claude_config(CLAUDE_LEGACY_CONFIG)
    if env:
        return (
            env.get("OKTOPOST_ACCOUNT_REGION", "us"),
            env.get("OKTOPOST_ACCOUNT_ID", ""),
            env.get("OKTOPOST_API_KEY", ""),
        )
    return "us", "", ""


def api_call(base_url, path, account_id, api_key):
    creds = base64.b64encode(f"{account_id}:{api_key}".encode()).decode()
    req = urllib.request.Request(f"{base_url}{path}", headers={"Authorization": f"Basic {creds}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def main():
    region, account_id, api_key = get_credentials()
    if not account_id or not api_key:
        print("ERROR: No credentials found. Set OKTOPOST_ACCOUNT_ID and OKTOPOST_API_KEY env vars,")
        print(f"       or run setup.py to configure {SETTINGS_PATH}")
        sys.exit(1)

    base_url = REGIONS.get(region, REGIONS["us"])
    print(f"Validating Oktopost connection (region: {region})...\n")

    try:
        me = api_call(base_url, "/v2/me", account_id, api_key)
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} - {e.reason}"); sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}"); sys.exit(1)

    acct = me.get('Account', {})
    user = me.get('User', {})
    print(f"Account:        {acct.get('Name', me.get('accountName', 'N/A'))}")
    print(f"API key owner:  {user.get('Name', me.get('userName', 'N/A'))}")
    print(f"Region:         {region.upper()}")
    print("Timezone:       (not returned by API -- set in preset's account.timezone)")

    try:
        profiles = api_call(base_url, "/v2/credential?_count=100", account_id, api_key)
    except Exception as e:
        print(f"\nWARNING: Could not fetch profiles: {e}")
        sys.exit(0)

    items = profiles if isinstance(profiles, list) else profiles.get("items", profiles.get("data", []))
    by_network = {}
    for p in items:
        net = p.get("network", p.get("type", "unknown"))
        by_network.setdefault(net, []).append(p)

    print(f"Profiles: {len(items)} total")
    for net, profs in sorted(by_network.items()):
        print(f"  {net}: {len(profs)}")

    print("\nConnection OK")


if __name__ == "__main__":
    main()
