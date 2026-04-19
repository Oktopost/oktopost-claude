# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-19

### Fixed
- REST fallback profiles endpoint is `/v2/credential`, not `/v2/social-profile` — the latter silently returns empty. Updated `publish.py`, `validate.py`, `api-fallback.md`.
- REST fallback `_count` page size: valid values are 25/50/100 only; values below 25 are rejected. Pre-flight check now uses `_count=25`.
- `/v2/me` does not return a timezone field — stopped claiming it does. Timezone is now asked from the user and stored in the preset's `account.timezone` field.
- MCP tool reference (`references/mcp-tools.md`) reconciled with the actual MCP tool list: renamed `list_inbox_tags` → `list_conversation_tags`, `create_case` → `create_salesforce_case`; dropped `send_feedback`; added `get_post_analytics`, `change_post_campaign`, `delete_post`, `delete_message`, `delete_campaign`, `delete_board_story`, `delete_board_topic`, `delete_advocate`, canned-response CRUD, and full conversation CRUD.
- `publish.py` payload format now matches Oktopost REST conventions (PascalCase `CampaignId`, `MessageId`, `Credentials[]`, `Network`, `StartDateTime`); earlier version would 400 on every call.
- Scripts now read credentials from `~/.claude.json` (where `claude mcp add` writes) with `~/.claude/settings.json` as a legacy fallback.
- Example preset no longer auto-copied into `~/.oktopost/presets/` on install — its `REPLACE_WITH_PROFILE_ID` placeholders would deadlock the runtime validator. Template lives in the skill dir as a reference.
- Preset validator now warns-and-skips placeholder presets instead of hard-blocking, unless the user explicitly `preset use`s one.
- `approval_required` default in the example preset flipped to `false` (was `true` — surprised first-time users when nothing published directly).

### Added
- Step 0 pre-flight connection check: verifies MCP is connected before any operation, cached per session.
- Media upload workflow: `create_media`, `create_upload`, `validate_video_upload` documented in Publishing and Campaign modes (images, video, LinkedIn PDF carousels).
- Approval workflow discovery: `list_workflows` pattern before first `send_to_workflow` call; asks user to pick when multiple workflows exist.
- Write-path smoke test during setup: `create_message` + `delete_message` on a dedicated check campaign before declaring setup complete.
- Non-interactive setup: `/oktopost setup --key <k> --account <id> --region <us|eu>` for key rotation and scripted provisioning.
- `--yes` / `-y` flag on write commands to skip the interactive confirm step; non-bypassable guardrails (approval routing, validation, destructive deletes) still run.
- `/oktopost help` subcommand with per-command examples.
- Post-publish undo pattern: `delete_post` recovery flow when the user regrets a just-scheduled post.
- REST fallback invocation recipe in SKILL.md §7: how and when to call `publish.py` / `report.py` / `validate.py` from inside a Claude Code session.
- Subagent delegation patterns documented for `oktopost-content-strategist` and `oktopost-analytics-interpreter` with explicit Agent tool prompt templates.

### Changed
- Hosted OAuth (`mcp.oktopost.com`) removed from all setup paths — Oktopost does not offer hosted OAuth. Local API key is the only supported path.
- Credentials URL updated to `https://app.oktopost.com/my-profile/api` (was "Settings > Integrations > API" — old UI location).
- UTM handling: skill no longer adds or prompts for UTMs. Oktopost auto-appends UTMs to every okt.to shortened link at publish time; manual UTMs produce double-UTMs and break attribution.
- Pre-flight reference loading: `mcp-tools.md` loads once per session (was every turn); `social-networks.md` loads only when the workflow touches a network.
- Response format contract scoped to writes only; reads use a lighter format.
- `/v2/me` user field now labeled "API key owner" (not "User") — reflects what the field actually represents.
- "Restart Claude Code" language softened — Claude Code usually hot-loads new MCP tools within seconds; restart only if they don't appear.
- Preset bootstrap writes to `<slug>.json`; no longer edits the example preset in place.
- Plaintext credential storage surfaced in setup output with rotation suggestion.

## [1.0.0] - 2026-04-17

### Added
- Core skill with 8 workflow modes: Publishing, Campaign, Analytics, Advocacy, Inbox, Calendar, Approval, Dashboard
- Brand preset system with team and personal preset support
- Multi-account support via preset-based account switching
- Reference documentation: MCP tools, social network specs, workflows, analytics benchmarks, API fallback
- Content strategist and analytics interpreter subagents (Sonnet)
- Python fallback scripts (stdlib only): setup, validate, publish, report
- Standalone installer with MCP configuration and uninstall support
- Plugin marketplace manifest
- Example brand preset (oktopost-example.json)
