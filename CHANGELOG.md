# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-09-10

### Fixed
- **Both plugin manifests failed `claude plugin validate`.** `plugin.json`: `author` must be an object, not a string, and `skills`/`agents` paths need a `./` prefix. `marketplace.json` was shaped like a plugin entry rather than a marketplace — no `owner`, no `plugins[]` — so `/plugin marketplace add` would have rejected it; ten of its keys were silently ignored.
- **The plugin never configured an MCP server.** `plugin.json` carried an `"mcp"` block that is not part of the plugin schema and was ignored at load time. MCP servers ship as a `.mcp.json` at the plugin root; added one.
- **`install.sh` never installed the subagents.** It copied only `skills/oktopost`, so every `oktopost-content-strategist` / `oktopost-analytics-interpreter` delegation failed at runtime. It now installs both, removes them on uninstall, and prunes `__pycache__` from the copied tree.
- **`references/mcp-tools.md` was substantially wrong.** Audited all 73 documented entries against the server's own `tools/list` schemas: 53 had incorrect parameters and 25 were missing a required parameter, meaning a call built from the reference failed outright. Worst offenders were on the hot path — `create_post` documented `profileId`/`network`/`scheduledAt` (real: `credentialIds`/`startDateTime`), `create_message` omitted the required `network` and called the body `body` (real: `message`), `get_calendar` documented `startDate`/`endDate` (real: `fromDate`/`toDate`), `send_to_workflow` documented `postId` (real: `entityId`), `create_media` documented `url`+`type` (real: `resource`). The parameter tables are now generated from the live schemas and cover all 85 tools with zero drift.
- `create_post`'s "each post targets exactly one profile" note was wrong — `credentialIds` is a comma-separated string that fans one message out to many profiles in a single call. Its "REST mapping" note described parameters that never existed; corrected in both `mcp-tools.md` and `api-fallback.md`.
- `SKILL.md` media flow passed `create_message({ assets: [...] })`; the real parameter is `media` and it takes a single ID string. Multi-asset attachment is `create_board_story({ mediaIds: "id1,id2" })`.
- `SKILL.md` Dashboard mode called `get_dashboard_report_data(dashboardId, widgetId, startDate, endDate)`; the real signature is `(dashboardId, reportId)` with an optional `filter` object and no date arguments.
- `get_social_post` / `get_post` flag is `stats`, not `withStats`.
- **All three fallback scripts were broken against the live REST API.** They read a lowercase `items` envelope key; the API returns `Items`. `validate.py` therefore always reported 0 social profiles (real: 15), and `report.py --days N` always printed "No campaigns found" against a populated account. Verified fixed by running both against a live account.
- `report.py` also read `id`/`name`/`status`/`postCount` and a nested `stats` object; the real fields are `Id`/`Name`/`Status`/`TotalPosts`, with engagement counters (`Clicks`, `Converts`, `Likes`, `Comments`) flat on the post. `GET /v2/campaign/{id}` wraps its payload in a `Campaign` key. `Created` is a `"YYYY-MM-DD HH:MM:SS"` string, not an epoch, so the `--days` filter silently matched nothing.
- `report.py` no longer advertises an engagement rate: the REST API exposes no impressions field, so the old rate was always `N/A` by construction.
- **`api-fallback.md` documented `GET /v2/postlog?withStats=1&_page=0&_count=50`**, which 400s -- `postId` is required and the endpoint does not paginate. Corrected, along with the response envelope (`Postlogs`, not `Items`).
- `api-fallback.md` used integer placeholder IDs (`12345`, `67890`). Oktopost IDs are 15-character prefixed strings; a numeric ID fails with `Failed to parse id`. Replaced with realistic IDs and documented the prefix scheme.
- `SKILL.md` claimed "Oktopost does NOT offer hosted OAuth." Oktopost's own docs describe OAuth for cloud clients and HTTP Basic for automation platforms, and `mcp.oktopost.com` is live -- the `oktopost-mcp` package is a thin stdio proxy in front of it. The local API key remains the only path *for Claude Code*, which is now what the skill says.
- Pagination is not uniform and the blanket "`_page` only" rule was wrong: `list_workflow_items` uses bare `page`/`count`, `list_media_folders` uses `_start`/`_count`, `list_conversations` takes `_count` with no page param, and ten list tools take no pagination at all. Documented per-tool.

### Added
- 12 previously undocumented tools: custom calendar event CRUD (`create`/`get`/`list`/`update`/`delete_custom_calendar_event`), media folder CRUD (`create`/`get`/`list`/`rename`/`delete_media_folder`), `list_tags`, and `list_targeting_presets`.
- Calendar Mode now reads and writes custom calendar events, so milestones and launch dates appear alongside scheduled posts and explain posting gaps.
- Publishing Mode now checks `list_targeting_presets` for LinkedIn profiles and can apply one via `targetingPresetId` on `create_post` — only when the user picks it.
- `.mcp.json` at the plugin root, so `/plugin install` wires up the `oktopost` MCP server. It reads `OKTOPOST_API_KEY`, `OKTOPOST_ACCOUNT_ID`, and `OKTOPOST_ACCOUNT_REGION` from the environment; `/oktopost setup` remains the credentialed path and takes precedence.
- `delete_media_folder` cascade warning — it is the only delete in the API that does cascade, removing every child folder and asset.

### Changed
- `api-fallback.md` gained a response-envelope section: every response carries `Result`; collections return `Items` plus `Total`; single resources return a named key.
- README documents both install paths (plugin marketplace and standalone script), and the tool count is corrected from "~40" to 85.
- Dropped the unused `MCP_CONFIG` variable from `install.sh` and the empty `screenshots/` directory referenced by the old manifest.

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
