#!/usr/bin/env python3
"""Direct API fallback for publishing to Oktopost."""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

CLAUDE_MAIN_CONFIG = os.path.expanduser("~/.claude.json")
CLAUDE_LEGACY_CONFIG = os.path.expanduser("~/.claude/settings.json")
REGIONS = {"us": "https://api.oktopost.com", "eu": "https://api.eu.oktopost.com"}


def _from_claude_config(path):
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
    region = os.environ.get("OKTOPOST_ACCOUNT_REGION")
    account_id = os.environ.get("OKTOPOST_ACCOUNT_ID")
    api_key = os.environ.get("OKTOPOST_API_KEY")
    if account_id and api_key:
        return region or "us", account_id, api_key
    env = _from_claude_config(CLAUDE_MAIN_CONFIG) or _from_claude_config(CLAUDE_LEGACY_CONFIG)
    if env:
        return (
            env.get("OKTOPOST_ACCOUNT_REGION", "us"),
            env.get("OKTOPOST_ACCOUNT_ID", ""),
            env.get("OKTOPOST_API_KEY", ""),
        )
    return "us", "", ""


def api_call(base_url, path, account_id, api_key, method="GET", data=None):
    creds = base64.b64encode(f"{account_id}:{api_key}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(f"{base_url}{path}", data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


NETWORK_CANONICAL = {
    "linkedin": "LinkedIn",
    "twitter": "Twitter",
    "x": "Twitter",
    "facebook": "Facebook",
    "instagram": "Instagram",
}


def canonical_network(name):
    key = name.strip().lower()
    if key not in NETWORK_CANONICAL:
        print(f"ERROR: Unknown network '{name}'. Use one of: linkedin, twitter/x, facebook, instagram.")
        sys.exit(1)
    return NETWORK_CANONICAL[key]


def _items(payload):
    return payload if isinstance(payload, list) else payload.get("items", payload.get("data", []))


def _field(obj, *names):
    for n in names:
        if n in obj and obj[n] not in (None, ""):
            return obj[n]
    return None


def find_campaign(base_url, account_id, api_key, name):
    campaigns = api_call(base_url, "/v2/campaign", account_id, api_key)
    for c in _items(campaigns):
        cname = _field(c, "Name", "name") or ""
        if cname.lower() == name.lower():
            return c
    return None


def find_profile(base_url, account_id, api_key, network):
    target = canonical_network(network)
    profiles = api_call(base_url, "/v2/credential?_count=100", account_id, api_key)
    for p in _items(profiles):
        net = _field(p, "Network", "network", "type") or ""
        if str(net).lower() == target.lower():
            return p
    return None


def parse_schedule(schedule_str):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            dt = datetime.strptime(schedule_str, fmt)
            return int(dt.timestamp())
        except ValueError:
            continue
    print(f"ERROR: Cannot parse schedule datetime '{schedule_str}'")
    print("  Accepted formats: YYYY-MM-DD HH:MM:SS, YYYY-MM-DD HH:MM, ISO with T separator")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Publish content via Oktopost API")
    parser.add_argument("--campaign", required=True, help="Campaign name (created if it doesn't exist)")
    parser.add_argument("--content", required=True, help="Post text content")
    parser.add_argument("--network", required=True, help="Social network (e.g. linkedin, twitter, facebook)")
    parser.add_argument("--schedule", help="Schedule datetime (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without executing")
    args = parser.parse_args()

    region, account_id, api_key = get_credentials()
    if not account_id or not api_key:
        print("ERROR: No credentials found. Run setup.py or set env vars."); sys.exit(1)

    base_url = REGIONS.get(region, REGIONS["us"])
    schedule_epoch = parse_schedule(args.schedule) if args.schedule else None

    if args.dry_run:
        print("=== DRY RUN ===")
        print(f"  Campaign:  {args.campaign}")
        print(f"  Network:   {args.network}")
        print(f"  Content:   {args.content[:80]}{'...' if len(args.content) > 80 else ''}")
        if schedule_epoch:
            print(f"  Scheduled: {args.schedule} (epoch: {schedule_epoch})")
        else:
            print("  Scheduled: Immediate")
        print("\nActions that would be taken:")

    network_canonical = canonical_network(args.network)

    # Step 1: Find or create campaign
    print(f"\n1. Looking up campaign '{args.campaign}'...")
    campaign = find_campaign(base_url, account_id, api_key, args.campaign)
    if campaign:
        campaign_id = _field(campaign, "Id", "id")
        print(f"   Found campaign ID: {campaign_id}")
    elif args.dry_run:
        print(f"   Would create new campaign '{args.campaign}'")
        campaign_id = "<new>"
    else:
        print(f"   Creating campaign '{args.campaign}'...")
        result = api_call(base_url, "/v2/campaign", account_id, api_key, "POST", {"Name": args.campaign})
        campaign_id = _field(result, "Id", "id")
        print(f"   Created campaign ID: {campaign_id}")

    # Step 2: Find profile
    print(f"\n2. Finding {network_canonical} profile...")
    profile = find_profile(base_url, account_id, api_key, args.network)
    if not profile:
        print(f"   ERROR: No {network_canonical} profile connected in this account.")
        print("          Connect one in Oktopost > Settings > Social Profiles, then retry.")
        sys.exit(1)
    profile_id = _field(profile, "Id", "id")
    profile_name = _field(profile, "Name", "name", "displayName") or "N/A"
    print(f"   Found profile: {profile_name} (ID: {profile_id})")

    if args.dry_run:
        print("\n3. Would create message with provided content")
        print(f"4. Would create post linking message to profile on {network_canonical}")
        print("\n=== DRY RUN COMPLETE (no changes made) ===")
        return

    # Step 3: Create message (reusable content template)
    print("\n3. Creating message...")
    msg_payload = {"CampaignId": campaign_id, "Content": args.content}
    message = api_call(base_url, "/v2/message", account_id, api_key, "POST", msg_payload)
    message_id = _field(message, "Id", "id")
    print(f"   Created message ID: {message_id}")

    # Step 4: Create post (scheduled instance on a specific profile/network)
    print("\n4. Creating post...")
    post_payload = {
        "CampaignId": campaign_id,
        "MessageId": message_id,
        "Credentials": [str(profile_id)],
        "Network": network_canonical,
    }
    if schedule_epoch:
        post_payload["StartDateTime"] = schedule_epoch
    post = api_call(base_url, "/v2/post", account_id, api_key, "POST", post_payload)
    post_id = _field(post, "Id", "id")
    print(f"   Created post ID: {post_id}")

    print("\n=== Published successfully ===")
    print(f"  Campaign ID: {campaign_id}")
    print(f"  Message ID:  {message_id}")
    print(f"  Post ID:     {post_id}")
    print(f"  Network:     {network_canonical}")
    if schedule_epoch:
        print(f"  Scheduled:   {args.schedule} (epoch: {schedule_epoch})")
    else:
        print("  Scheduled:   Immediate (per account publishing defaults)")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as e:
        body = e.read().decode() if hasattr(e, "read") else ""
        print(f"\nAPI ERROR: HTTP {e.code} - {e.reason}")
        if body:
            print(f"  Response: {body[:300]}")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
