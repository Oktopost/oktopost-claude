#!/usr/bin/env python3
"""Direct API fallback for Oktopost analytics reporting."""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

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


def api_call(base_url, path, account_id, api_key):
    creds = base64.b64encode(f"{account_id}:{api_key}".encode()).decode()
    req = urllib.request.Request(f"{base_url}{path}", headers={"Authorization": f"Basic {creds}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def fmt_num(n):
    return "{:,}".format(n) if isinstance(n, int) else str(n)


def print_table(headers, rows, col_widths=None):
    if not col_widths:
        col_widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) for i, h in enumerate(headers)]
    header_line = "  ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("  ".join("-" * w for w in col_widths))
    for row in rows:
        print("  ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(headers))))


def campaign_report(base_url, account_id, api_key, campaign_id):
    campaign = api_call(base_url, f"/v2/campaign/{campaign_id}", account_id, api_key)
    print(f"Campaign: {campaign.get('name', 'N/A')} (ID: {campaign_id})")
    print(f"Status:   {campaign.get('status', 'N/A')}\n")

    posts = api_call(base_url, f"/v2/post?campaignId={campaign_id}&_count=100", account_id, api_key)
    items = posts if isinstance(posts, list) else posts.get("items", posts.get("data", []))

    if not items:
        print("No posts found for this campaign.")
        return

    totals = {"clicks": 0, "conversions": 0, "likes": 0, "comments": 0, "impressions": 0, "posts": len(items)}
    rows = []
    for p in items:
        stats = p.get("stats", p.get("statistics", {}))
        clicks = stats.get("clicks", 0)
        convs = stats.get("conversions", 0)
        likes = stats.get("likes", stats.get("reactions", 0))
        comments = stats.get("comments", stats.get("replies", 0))
        impressions = stats.get("impressions", 0)
        network = p.get("network", p.get("type", "?"))
        content = p.get("content", p.get("text", ""))[:40]
        eng_rate = f"{((likes + comments + clicks) / impressions * 100):.1f}%" if impressions > 0 else "N/A"

        rows.append([network, content, fmt_num(clicks), fmt_num(convs), fmt_num(likes), fmt_num(comments), eng_rate])
        totals["clicks"] += clicks
        totals["conversions"] += convs
        totals["likes"] += likes
        totals["comments"] += comments
        totals["impressions"] += impressions

    headers = ["Network", "Content", "Clicks", "Convs", "Likes", "Comments", "Eng%"]
    print_table(headers, rows, [10, 42, 8, 8, 8, 10, 8])

    total_eng = totals["clicks"] + totals["likes"] + totals["comments"]
    total_eng_rate = f"{(total_eng / totals['impressions'] * 100):.1f}%" if totals["impressions"] > 0 else "N/A"
    print(f"\nTotals: {totals['posts']} posts | {fmt_num(totals['clicks'])} clicks | "
          f"{fmt_num(totals['conversions'])} conversions | {fmt_num(totals['likes'])} likes | "
          f"{fmt_num(totals['comments'])} comments | Engagement: {total_eng_rate}")


def list_campaigns(base_url, account_id, api_key, days):
    campaigns = api_call(base_url, "/v2/campaign?_count=50", account_id, api_key)
    items = campaigns if isinstance(campaigns, list) else campaigns.get("items", campaigns.get("data", []))

    cutoff = int(time.time()) - (days * 86400)
    filtered = []
    for c in items:
        created = c.get("createdAt", c.get("created_at", 0))
        if isinstance(created, str):
            filtered.append(c)  # can't filter string dates, include them
        elif created >= cutoff or cutoff == 0:
            filtered.append(c)

    if not filtered:
        print(f"No campaigns found in the last {days} days.")
        return

    print(f"Recent campaigns (last {days} days):\n")
    rows = []
    for c in filtered[:25]:
        cid = c.get("id", "?")
        name = c.get("name", "N/A")[:35]
        status = c.get("status", "?")
        post_count = c.get("postCount", c.get("post_count", "?"))
        rows.append([str(cid), name, status, str(post_count)])

    headers = ["ID", "Name", "Status", "Posts"]
    print_table(headers, rows, [10, 37, 10, 8])
    print(f"\nRun with --campaign <ID> for detailed stats.")


def main():
    parser = argparse.ArgumentParser(description="Oktopost analytics report")
    parser.add_argument("--campaign", help="Campaign ID for detailed report")
    parser.add_argument("--days", type=int, default=30, help="Filter campaigns by age (default: 30)")
    args = parser.parse_args()

    region, account_id, api_key = get_credentials()
    if not account_id or not api_key:
        print("ERROR: No credentials found. Run setup.py or set env vars."); sys.exit(1)

    base_url = REGIONS.get(region, REGIONS["us"])

    try:
        if args.campaign:
            campaign_report(base_url, account_id, api_key, args.campaign)
        else:
            list_campaigns(base_url, account_id, api_key, args.days)
    except urllib.error.HTTPError as e:
        body = e.read().decode() if hasattr(e, "read") else ""
        print(f"API ERROR: HTTP {e.code} - {e.reason}")
        if body:
            print(f"  Response: {body[:300]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
