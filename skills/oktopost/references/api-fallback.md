# Oktopost REST API — Direct Fallback Reference

Use this reference when the Oktopost MCP server is unavailable, not configured, not responding, or rate-limited. These endpoints allow direct REST calls to accomplish common operations.

## Base URLs

| Region | Base URL |
|---|---|
| US | `https://api.oktopost.com/v2` |
| EU | `https://eu-api.oktopost.com/v2` |

## Authentication

HTTP Basic Auth on every request:

```
Authorization: Basic <base64(AccountId:ApiKey)>
```

Find credentials at https://app.oktopost.com/my-profile/api (log in first). The AccountId is the numeric account identifier, and the ApiKey is the generated token.

## Key Endpoints

### Account Verification

```
GET /v2/me
```

Returns account info. Use to verify credentials and connectivity.

### Campaigns

```
GET  /v2/campaign?_page=0&_count=25
POST /v2/campaign
```

Create body:
```json
{
  "Name": "Campaign Name",
  "Url": "https://example.com/landing",
  "Tags": ["tag1", "tag2"],
  "StartDate": 1718841600,
  "EndDate": 1721520000,
  "Utm": { "source": "oktopost", "medium": "social" }
}
```

### Messages

```
GET  /v2/message?campaignId=12345
POST /v2/message
```

Messages are the content templates attached to campaigns.

### Posts

```
GET  /v2/post?campaignId=12345
POST /v2/post
GET  /v2/post/{id}?withStats=1
```

Create body:
```json
{
  "CampaignId": 12345,
  "MessageId": 67890,
  "Credentials": ["profile-id-1"],
  "Network": "LinkedIn",
  "StartDateTime": 1718841600
}
```

**MCP mapping:** The `create_post` MCP tool accepts `messageId`, `profileId`, `network`, `scheduledAt` (camelCase). The MCP server flattens those to the PascalCase REST payload above — `profileId` becomes `Credentials: [profileId]`, `scheduledAt` becomes `StartDateTime`. Prefer the MCP tool unless you are in fallback mode.

### Published Posts (Post Log)

```
GET /v2/postlog?withStats=1&_page=0&_count=50
```

Returns published posts with engagement statistics. Use for reporting and analytics.

### Social Profiles

```
GET /v2/credential
```

Returns all connected social profiles with IDs, network type, and status. Use the returned IDs as the `Credentials` array when creating posts.

**Gotcha:** This endpoint is NOT `/v2/social-profile` (that returns an empty `{"Result":false,"Errors":[]}`). The MCP tool is called `list_social_profiles` but the REST URL path is `/v2/credential`.

### Workflow (Approval Queue)

```
GET  /v2/workflow-item
POST /v2/workflow-item/{id}
```

Process body:
```json
{
  "action": "approve",
  "note": "Looks good, approved."
}
```

Action values: `approve` or `reject`.

### Content Boards

```
GET  /v2/board
POST /v2/board/{id}/story
```

Create stories (content items) within a specific board.

### Conversations

```
GET /v2/conversation
```

Returns social conversations for monitoring and engagement.

## Pagination

All list endpoints accept:

| Param | Description |
|---|---|
| `_page` | Page number, 0-indexed |
| `_count` | Results per page: 25, 50, or 100 |

## Rate Limits

| Window | Limit |
|---|---|
| Per day | 20,000 requests |
| Per minute | 60 requests |
| Per 5 seconds | 120 requests |

A `429 Too Many Requests` response means you hit a limit. Back off and retry. Sustained overage triggers a 15-minute block on the API key.

## Important Conventions

- **Timestamps:** All date/time values are Unix epoch in **seconds** (not milliseconds). Divide JS `Date.now()` by 1000.
- **Error format:** JSON body with an error message field. Standard HTTP status codes (400, 401, 403, 404, 429, 500).
- **Network values:** `LinkedIn`, `Twitter`, `Facebook`, `Instagram` (case-sensitive strings).

## Fallback Scripts

For automated workflows when the MCP server is down:

- **Publishing:** `scripts/publish.py` — queues and publishes posts via direct API
- **Reporting:** `scripts/report.py` — pulls post log and generates performance summaries

Both scripts read credentials from environment variables `OKTOPOST_ACCOUNT_ID` and `OKTOPOST_API_KEY`.
