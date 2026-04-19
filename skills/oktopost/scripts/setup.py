#!/usr/bin/env python3
"""Interactive setup wizard for Oktopost MCP connection."""

import base64
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import urllib.error

CLAUDE_MAIN_CONFIG = os.path.expanduser("~/.claude.json")            # primary MCP config
CLAUDE_LEGACY_CONFIG = os.path.expanduser("~/.claude/settings.json")  # legacy
PRESETS_DIR = os.path.expanduser("~/.oktopost/presets")
REGIONS = {"us": "https://api.oktopost.com", "eu": "https://api.eu.oktopost.com"}
MCP_SERVER_NAME = "oktopost"


def load_settings():
    """Return (settings_dict, source_path) for whichever Claude Code config holds the oktopost MCP.

    Prefers ~/.claude.json (where `claude mcp add` writes). Falls back to
    ~/.claude/settings.json for older setups.
    """
    for path in (CLAUDE_MAIN_CONFIG, CLAUDE_LEGACY_CONFIG):
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f), path
            except (OSError, json.JSONDecodeError):
                continue
    return {}, None


def api_call(base_url, path, account_id, api_key):
    creds = base64.b64encode(f"{account_id}:{api_key}".encode()).decode()
    req = urllib.request.Request(f"{base_url}{path}", headers={"Authorization": f"Basic {creds}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def get_mcp_config(settings):
    servers = settings.get("mcpServers", {})
    return servers.get(MCP_SERVER_NAME) or servers.get("oktopost-mcp")


def register_mcp_via_cli(account_id, api_key, region):
    if shutil.which("claude") is None:
        print("ERROR: Claude Code CLI ('claude') not found on PATH.")
        print("Install it from https://docs.anthropic.com/en/docs/claude-code and re-run.")
        sys.exit(1)

    if shutil.which("npx") is None:
        print("ERROR: 'npx' not found on PATH.")
        print("Install Node.js 20+ (https://nodejs.org) so the oktopost-mcp server can run.")
        sys.exit(1)

    subprocess.run(["claude", "mcp", "remove", MCP_SERVER_NAME],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    cmd = ["claude", "mcp", "add", MCP_SERVER_NAME,
           "-e", f"OKTOPOST_ACCOUNT_ID={account_id}",
           "-e", f"OKTOPOST_API_KEY={api_key}"]
    if region and region != "us":
        cmd += ["-e", f"OKTOPOST_ACCOUNT_REGION={region}"]
    cmd += ["--", "npx", "oktopost-mcp"]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: 'claude mcp add' failed (exit {e.returncode}).")
        print("Possible causes:")
        print("  - The 'oktopost-mcp' npm package is not yet available in your registry.")
        print("  - Claude Code CLI version does not support the 'mcp add' subcommand.")
        print("You can still use the skill in fallback mode via the REST API scripts in")
        print(f"  ~/.claude/skills/oktopost/scripts/ (publish.py, report.py).")
        sys.exit(1)


def validate_connection(base_url, account_id, api_key):
    try:
        data = api_call(base_url, "/v2/me", account_id, api_key)
        return data
    except urllib.error.HTTPError as e:
        print(f"  ERROR: HTTP {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def main():
    print("=== Oktopost MCP Setup Wizard ===\n")
    settings, settings_path = load_settings()
    mcp = get_mcp_config(settings)

    if mcp:
        print(f"Found existing oktopost-mcp configuration in {settings_path}.")
        env = mcp.get("env", {})
        region = env.get("OKTOPOST_ACCOUNT_REGION", "us")
        account_id = env.get("OKTOPOST_ACCOUNT_ID", "")
        api_key = env.get("OKTOPOST_API_KEY", "")
        if account_id and api_key:
            base_url = REGIONS.get(region, REGIONS["us"])
            print(f"  Validating connection ({region})...")
            me = validate_connection(base_url, account_id, api_key)
            if me:
                acct = me.get('Account', {})
                user = me.get('User', {})
                print(f"  Connected! Account: {acct.get('Name', me.get('accountName', 'N/A'))}")
                print(f"  API key owner: {user.get('Name', me.get('userName', 'N/A'))}")
                print("  Timezone:  (not returned by /v2/me -- set per preset in ~/.oktopost/presets/<brand>.json)")
                check_presets()
                return
            print("  Existing credentials are invalid. Let's reconfigure.\n")
        else:
            print("  Credentials incomplete. Let's reconfigure.\n")
    else:
        print("No existing oktopost-mcp configuration found.\n")

    print("Setup: local API key (find it at https://app.oktopost.com/my-profile/api).")
    region = input("\nRegion (us/eu) [us]: ").strip().lower() or "us"
    if region not in REGIONS:
        print(f"Invalid region '{region}'. Use 'us' or 'eu'."); sys.exit(1)
    account_id = input("Account ID: ").strip()
    api_key = input("API Key: ").strip()
    if not account_id or not api_key:
        print("Account ID and API Key are required."); sys.exit(1)

    base_url = REGIONS[region]
    print(f"\nValidating connection ({region})...")
    me = validate_connection(base_url, account_id, api_key)
    if not me:
        print("Connection failed. Check your credentials."); sys.exit(1)

    acct = me.get('Account', {})
    user = me.get('User', {})
    print(f"Connected! Account: {acct.get('Name', me.get('accountName', 'N/A'))}")
    print(f"API key owner: {user.get('Name', me.get('userName', 'N/A'))}")
    print("Timezone:  (not returned by /v2/me -- set it in your preset's account.timezone field)")

    register_mcp_via_cli(account_id, api_key, region)
    print(f"\nMCP server '{MCP_SERVER_NAME}' registered via 'claude mcp add'.")
    print("Claude Code should hot-load the new server within a few seconds.")
    print("If the oktopost tools don't appear, restart Claude Code once.")
    check_presets()


def check_presets():
    if os.path.isdir(PRESETS_DIR) and os.listdir(PRESETS_DIR):
        print(f"\nPresets found in {PRESETS_DIR}")
    else:
        print(f"\nNo presets found in {PRESETS_DIR}")
        print("Consider creating presets to speed up common publishing workflows.")


if __name__ == "__main__":
    main()
