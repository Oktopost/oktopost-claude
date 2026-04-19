# Oktopost MCP Tools Reference

> Authoritative reference for the `oktopost-mcp` npm package. Read this before every Oktopost API operation.

---

## Global API conventions

| Convention | Detail |
|---|---|
| **Timestamps** | Unix epoch **seconds** (not milliseconds, not ISO-8601). Always divide JS `Date.now()` by 1000 when passing dates. |
| **Pagination** | `_page` (0-indexed) + `_count` (25, 50, or 100 ONLY; default 25). Offset-based only. Any value below 25 (including `_count=1`) is rejected with "Page size X is not valid." -- use 25 as the minimum, even for liveness checks. |
| **Updates** | POST to `/{resource}/{id}` (not PUT/PATCH). |
| **Message vs Post** | A **Message** is reusable content (text + assets). A **Post** is a scheduled or published instance tied to a specific social profile. |
| **IDs** | All resource IDs are strings. |
| **Errors** | Non-2xx responses return `{ error: string, statusCode: number }`. |

---

## Campaigns

### `list_campaigns`

List all campaigns with optional filters.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page (25/50/100) |
| `withStats` | boolean | | Include engagement stats per campaign |

**Returns:** Array of campaign objects (`id`, `name`, `createdAt`, `updatedAt`, `status`, optional `stats`).

### `get_campaign_by_id`

Retrieve a single campaign by ID.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string | * | Campaign ID |

**Returns:** Full campaign object with metadata and optional stats.

### `create_campaign`

Create a new campaign.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | * | Campaign name |

**Returns:** Created campaign object with generated `id`.

### `update_campaign`

Update an existing campaign.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string | * | Campaign ID |
| `name` | string | | New campaign name |

**Returns:** Updated campaign object.

**Note:** Updating a campaign does not cascade changes to its posts or messages.

### `delete_campaign`

Delete a campaign. Does NOT cascade — posts and messages remain but become orphaned. Re-assign them with `change_post_campaign` first if you care about attribution.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string | * | Campaign ID |

**Returns:** Confirmation.

---

## Messages

Messages are reusable content templates. Posts are created from messages.

### `list_messages`

List messages with optional filters.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string | | Filter by campaign |
| `withTags` | boolean | | Include tag metadata |
| `withAssets` | boolean | | Include attached media assets |
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of message objects (`id`, `campaignId`, `body`, `createdAt`, `updatedAt`, optional `tags`, optional `assets`).

### `get_message_by_id`

Retrieve a single message.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `messageId` | string | * | Message ID |

**Returns:** Full message object.

### `create_message`

Create a new message.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string | * | Parent campaign ID |
| `body` | string | * | Message text content |
| `tags` | string[] | | Tag IDs to attach |
| `assets` | string[] | | Media asset IDs to attach |

**Returns:** Created message object with generated `id`.

### `update_message`

Update an existing message.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `messageId` | string | * | Message ID |
| `body` | string | | Updated text content |
| `tags` | string[] | | Updated tag IDs |
| `assets` | string[] | | Updated asset IDs |

**Returns:** Updated message object.

### `delete_message`

Delete a message. Posts previously created from this message remain intact.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `messageId` | string | * | Message ID |

**Returns:** Confirmation.

---

## Posts

Posts are scheduled or published instances of messages on specific social profiles.

### `list_posts`

List posts (internal/draft posts).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string | | Filter by campaign |
| `messageId` | string | | Filter by parent message |
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of post objects (`id`, `messageId`, `campaignId`, `profileId`, `scheduledAt`, `status`, `body`).

### `get_post`

Retrieve a single post.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | Post ID |

**Returns:** Full post object.

### `create_post`

Create and schedule a post on a social profile.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `messageId` | string | * | Parent message ID |
| `profileId` | string | * | Target social profile ID |
| `network` | string | * | Network name — `LinkedIn`, `Twitter`, `Facebook`, `Instagram` (case-sensitive) |
| `scheduledAt` | number | * | Publish time as Unix epoch **seconds** |
| `body` | string | | Override message body for this post |

**Returns:** Created post object with generated `id`.

**Note:** Each post targets exactly one profile. To publish the same message to multiple profiles, create one post per profile.

**REST mapping:** The MCP flattens the REST payload. Under the hood `profileId` is sent as `Credentials: [profileId]` and `scheduledAt` as `StartDateTime` — see `references/api-fallback.md` if you call the REST API directly.

### `update_post`

Update a scheduled (unpublished) post.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | Post ID |
| `scheduledAt` | number | | New scheduled time (epoch seconds) |
| `body` | string | | Updated body text |

**Returns:** Updated post object.

**Note:** Published posts cannot be updated — only deleted.

### `list_social_posts`

List published social posts with engagement data.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string | | Filter by campaign |
| `profileId` | string | | Filter by profile |
| `withStats` | boolean | | Include engagement metrics |
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of social post objects with optional stats (impressions, clicks, likes, shares, comments).

### `get_social_post`

Retrieve a single published social post.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `socialPostId` | string | * | Social post ID |

**Returns:** Full social post object with engagement data.

### `get_post_analytics`

Retrieve engagement analytics for a specific post (scheduled or published).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | Post ID |
| `startDate` | number | | Start of range (epoch seconds) |
| `endDate` | number | | End of range (epoch seconds) |

**Returns:** Analytics object (impressions, clicks, conversions, likes, comments, shares).

**Note:** Stats for freshly-published posts can lag by up to 24 hours depending on the source network.

### `change_post_campaign`

Re-assign an existing post to a different campaign. Use to fix attribution when a post was created under the wrong campaign.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | Post ID |
| `campaignId` | string | * | Target campaign ID |

**Returns:** Updated post object.

### `delete_post`

Delete a post. Works for both scheduled and published posts.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | Post ID |

**Returns:** Confirmation.

**Note:** Deleting a published post removes it from Oktopost's records but does not retract the already-published social post on the network. Deletion on the network must be done manually where the platform allows.

---

## Media and uploads

### `list_media`

List media assets in the library.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of media objects (`id`, `url`, `type`, `filename`, `createdAt`).

### `get_media`

Retrieve a single media asset.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `mediaId` | string | * | Media ID |

**Returns:** Full media object.

### `create_media`

Create a media asset from a URL.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | * | Public URL of the media file |
| `type` | string | * | Media type (e.g., `image`, `video`, `gif`) |

**Returns:** Created media object with generated `id`.

### `list_uploads`

List file uploads.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of upload objects.

### `get_upload`

Retrieve a single upload.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `uploadId` | string | * | Upload ID |

**Returns:** Full upload object.

### `create_upload`

Initiate a file upload.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `filename` | string | * | File name |
| `contentType` | string | * | MIME type |

**Returns:** Upload object with a signed upload URL.

### `validate_video_upload`

Validate a video upload meets platform requirements.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `uploadId` | string | * | Upload ID to validate |

**Returns:** Validation result (`valid`, `errors`).

---

## Calendar

### `get_calendar`

Retrieve the publishing calendar for a date range.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `startDate` | number | * | Start of range (epoch seconds) |
| `endDate` | number | * | End of range (epoch seconds) |
| `campaignId` | string | | Filter by campaign |
| `profileId` | string | | Filter by profile |

**Returns:** Array of scheduled and published posts within the date range.

---

## Social profiles

### `list_social_profiles`

List all connected social profiles.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of profile objects (`id`, `name`, `network`, `type`, `imageUrl`, `status`).

### `get_social_profile`

Retrieve a single social profile.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `profileId` | string | * | Profile ID |

**Returns:** Full profile object.

---

## Approvals and workflows

### `list_workflows`

List all approval workflows.

**Returns:** Array of workflow objects (`id`, `name`, `steps`).

### `get_workflow`

Retrieve a single workflow.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `workflowId` | string | * | Workflow ID |

**Returns:** Full workflow object with step definitions.

### `list_workflow_items`

List items pending in a workflow.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `workflowId` | string | * | Workflow ID |
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of workflow item objects (`id`, `status`, `postId`, `currentStep`).

### `process_workflow_item`

Approve or reject a workflow item.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `workflowItemId` | string | * | Workflow item ID |
| `action` | string | * | `approve` or `reject` |
| `note` | string | | Optional note explaining the decision |

**Returns:** Updated workflow item.

### `list_workflow_item_notes`

List notes on a workflow item.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `workflowItemId` | string | * | Workflow item ID |

**Returns:** Array of note objects.

### `add_workflow_item_note`

Add a note to a workflow item.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `workflowItemId` | string | * | Workflow item ID |
| `note` | string | * | Note text |

**Returns:** Created note object.

### `send_to_workflow`

Submit a post to a workflow for approval.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | Post ID to submit |
| `workflowId` | string | * | Target workflow ID |

**Returns:** Created workflow item.

### `remove_from_workflow`

Remove a post from its current workflow.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `workflowItemId` | string | * | Workflow item ID to remove |

**Returns:** Confirmation of removal.

---

## Employee advocacy

### Boards

#### `list_boards`

List all advocacy boards.

**Returns:** Array of board objects (`id`, `name`, `description`).

#### `get_board`

Retrieve a single board.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string | * | Board ID |

**Returns:** Full board object.

### Board topics

#### `list_board_topics`

List topics within a board.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string | * | Board ID |

**Returns:** Array of topic objects.

#### `create_board_topic`

Create a new topic in a board.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string | * | Board ID |
| `name` | string | * | Topic name |

**Returns:** Created topic object.

#### `update_board_topic`

Update a board topic.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `topicId` | string | * | Topic ID |
| `name` | string | | Updated topic name |

**Returns:** Updated topic object.

### Board stories

#### `list_board_stories`

List stories in a board.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string | * | Board ID |
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of story objects (`id`, `boardId`, `title`, `body`, `url`, `createdAt`).

#### `get_board_story`

Retrieve a single board story.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `storyId` | string | * | Story ID |

**Returns:** Full story object.

#### `create_board_story`

Create a new story in a board.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string | * | Board ID |
| `title` | string | * | Story title |
| `body` | string | | Story body/description |
| `url` | string | | Link URL for the story |
| `topicId` | string | | Topic to assign the story to |

**Returns:** Created story object.

#### `update_board_story`

Update an existing board story.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `storyId` | string | * | Story ID |
| `title` | string | | Updated title |
| `body` | string | | Updated body |
| `url` | string | | Updated URL |

**Returns:** Updated story object.

#### `delete_board_story`

Delete a board story. Does not affect advocates who already shared it.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `storyId` | string | * | Story ID |

**Returns:** Confirmation.

#### `delete_board_topic`

Delete a board topic. Stories assigned to the topic are not deleted — they become untagged.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `topicId` | string | * | Topic ID |

**Returns:** Confirmation.

### Advocates

#### `list_advocates`

List advocates (employees) in the advocacy program.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of advocate objects (`id`, `name`, `email`, `status`).

#### `get_advocate`

Retrieve a single advocate.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `advocateId` | string | * | Advocate ID |

**Returns:** Full advocate object.

#### `invite_advocate`

Invite a new employee to the advocacy program.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | string | * | Invitee email address |
| `name` | string | * | Invitee full name |

**Returns:** Created advocate invitation.

#### `delete_advocate`

Remove an advocate from the program.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `advocateId` | string | * | Advocate ID |

**Returns:** Confirmation.

---

## Users

### `list_users`

List users in the Oktopost organization.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of user objects (`id`, `name`, `email`, `role`).

### `get_user`

Retrieve a single user.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `userId` | string | * | User ID |

**Returns:** Full user object.

---

## Social BI (added in v2.8.0)

Dashboard and reporting tools for social analytics.

### `list_dashboards`

List available Social BI dashboards.

**Returns:** Array of dashboard objects (`id`, `name`).

### `get_dashboard`

Retrieve a single dashboard.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dashboardId` | string | * | Dashboard ID |

**Returns:** Full dashboard object with widget definitions.

### `get_dashboard_report_data`

Retrieve report data from a dashboard widget.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dashboardId` | string | * | Dashboard ID |
| `widgetId` | string | * | Widget ID |
| `startDate` | number | | Start date (epoch seconds) |
| `endDate` | number | | End date (epoch seconds) |

**Returns:** Report data matching the widget configuration (metrics, dimensions, time series).

---

## Inbox (added in v2.7.0)

Social inbox and conversation management.

### `list_conversations`

List inbox conversations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `profileId` | string | | Filter by social profile |
| `status` | string | | Filter by status (`open`, `closed`) |
| `_page` | number | | Page number (0-indexed) |
| `_count` | number | | Results per page |

**Returns:** Array of conversation objects.

### `get_conversation`

Retrieve a single conversation by ID.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | Conversation ID |

**Returns:** Full conversation object.

### `get_conversation_timeline`

Retrieve the full message/activity timeline for a conversation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | Conversation ID |

**Returns:** Ordered array of timeline events (messages, assignments, status changes).

### `reply_to_conversation`

Post a reply into an existing conversation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | Conversation ID |
| `body` | string | * | Reply text |

**Returns:** Created reply object.

### `assign_conversation`

Assign a conversation to a user for follow-up.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | Conversation ID |
| `userId` | string | * | User ID to assign |

**Returns:** Updated conversation object.

### `update_conversation_status`

Change a conversation's status (open, closed, pending).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | Conversation ID |
| `status` | string | * | Target status |

**Returns:** Updated conversation object.

### `add_conversation_note`

Add an internal note (not visible to the public) to a conversation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | Conversation ID |
| `body` | string | * | Note text |

**Returns:** Created note object.

### Conversation tags

#### `list_conversation_tags`

List available conversation tags.

**Returns:** Array of tag objects (`id`, `name`, `color`).

#### `get_conversation_tag`

Retrieve a single tag.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tagId` | string | * | Tag ID |

**Returns:** Full tag object.

#### `update_conversation_tag`

Rename or recolor a single tag definition.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tagId` | string | * | Tag ID |
| `name` | string | | New tag name |
| `color` | string | | New tag color |

**Returns:** Updated tag object.

#### `update_conversation_tags`

Replace the set of tags attached to a conversation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | Conversation ID |
| `tagIds` | string[] | * | Full list of tag IDs to attach (replaces existing tags) |

**Returns:** Updated conversation object.

#### `delete_conversation_tag`

Delete a tag definition. Does not delete the conversations it was attached to.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tagId` | string | * | Tag ID |

**Returns:** Confirmation.

### Canned responses

#### `list_canned_responses`

List saved canned responses for quick replies.

**Returns:** Array of canned response objects (`id`, `title`, `body`).

#### `get_canned_response`

Retrieve a single canned response.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cannedResponseId` | string | * | Canned response ID |

**Returns:** Full canned response object.

#### `create_canned_response`

Create a new canned response template.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `title` | string | * | Short identifier shown in the reply picker |
| `body` | string | * | Response body text |

**Returns:** Created canned response object.

### Salesforce integration

#### `create_salesforce_case`

Create a Salesforce case from a conversation. Requires a connected Salesforce integration.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | Source conversation ID |
| `subject` | string | * | Case subject line |
| `description` | string | | Case description |

**Returns:** Created Salesforce case object with external case ID.

---

## What does NOT exist

These tools, parameters, and behaviors are **not available**. Do not hallucinate them.

### Non-existent tools
- **`bulk_publish`** or **`bulk_create`** — Posts must be created individually, one at a time.
- **`search_posts`** — There is no search tool. Filter results using query parameters on `list_posts` or `list_social_posts`.
- **`undo_publish`** — Published posts cannot be unpublished from the source network via API. `delete_post` removes the record from Oktopost but does not retract what's already live.
- **`A/B_test`** — There is no A/B test parameter on posts. A/B testing must be done manually by creating separate posts.
- **`send_feedback`** — Not exposed by the MCP server. Feedback goes through the Oktopost product directly.

### Cascading delete gotchas
- `delete_campaign` does NOT cascade. Posts and messages under it become orphaned. If you care about attribution, re-assign posts with `change_post_campaign` first.
- `delete_message` does NOT delete posts created from that message.
- `delete_board_topic` does NOT delete the stories tagged to it — they become untagged.

### Non-existent parameters
- **`numberOfImages`** — Does not exist on any tool.
- **`negativePrompt`** — Does not exist on any tool.
- **`seed`** — No reproducibility seed parameter exists.

### Unsupported behaviors
- **Cursor-based pagination** — Not supported. Use offset pagination with `_page` only.
- **Real-time analytics streaming** — Analytics data has daily granularity. There is no live streaming.
- **Direct Instagram Story publishing** — Stories cannot be published via the API.
