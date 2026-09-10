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

## Response envelopes

Every response carries a boolean `Result`. Collection endpoints return `Items`;
single-resource endpoints return a named key (`/v2/post/{id}` returns `Post`,
`/v2/postlog` returns `Postlogs`, `/v2/me` returns `User` and `Account`). Errors
return `Result: false` plus an `Errors` object keyed by failure type.

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
GET  /v2/message?campaignId=002rfet4s6n361h
POST /v2/message
```

Messages are the content templates attached to campaigns.

### Posts

```
GET  /v2/post?campaignId=002rfet4s6n361h
POST /v2/post
GET  /v2/post/{id}?withStats=1
```

Create body:
```json
{
  "CampaignId": "002rfet4s6n361h",
  "MessageId": "005k2p9wq4xd118",
  "Credentials": ["003-a1b2c3d4e5f6g7h"],
  "Network": "LinkedIn",
  "StartDateTime": 1718841600
}
```

**IDs are 15-character strings, not integers.** Campaigns start `002`, posts `004`,
messages `005`, social profiles `003-`. Passing a numeric ID fails with
`Failed to parse id` (posts) or ``` `campaignId` must be between 15 and 15
characters long ``` (messages).

**MCP mapping:** The `create_post` MCP tool accepts `messageId`, `credentialIds`, `startDateTime` (camelCase). The MCP server maps those onto the PascalCase REST payload above — `credentialIds` is a comma-separated string that becomes the `Credentials` array, and `startDateTime` becomes `StartDateTime`. Note there is no `network` argument on `create_post`; the network comes from the message. Prefer the MCP tool unless you are in fallback mode.

### Published Posts (Post Log)

```
GET /v2/postlog?postId={postId}&withStats=1
```

Returns the published instances of **one** post, with engagement statistics when
`withStats=1` is set. `postId` is required -- this is not a list-everything endpoint,
and calling it without one returns
`{"Result":false,"Errors":{"Param":{"get":"Missing value for parameter postId"}}}`.
It does not paginate. To sweep an account, iterate campaigns via `/v2/campaign`,
then posts via `/v2/post?campaignId={id}`, then postlogs per post.

The response envelope is `Postlogs`, not `Items`.

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
