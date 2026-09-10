# Oktopost MCP Tools Reference

> Authoritative reference for the tools exposed by the `oktopost-mcp` package.
> Read this before every Oktopost API operation.
>
> Parameter tables in this file are generated from the server's own tool schemas
> (`tools/list`), so they match what the server actually accepts. Regenerate them
> whenever the server adds tools or changes parameters -- do not hand-edit the tables.

---

## Global API conventions

| Convention | Detail |
|---|---|
| **Timestamps** | Unix epoch **seconds** (not milliseconds, not ISO-8601). Always divide JS `Date.now()` by 1000 when passing dates. |
| **Pagination** | Offset-based, but not uniform -- always check the tool's own table. Most list tools take `_page` (0-indexed) + `_count`; `list_workflow_items` uses bare `page`/`count`; `list_media_folders` uses `_start`/`_count`; `list_conversations` takes `_count` with no page param. Ten list tools take no pagination at all, including `list_messages`, `list_media`, `list_social_posts`, `list_social_profiles`, `list_workflows` and `list_targeting_presets`. Where `_count` is constrained it is 25, 50 or 100 only (default 25) and smaller values are rejected with "Page size X is not valid." |
| **Updates** | POST to `/{resource}/{id}` (not PUT/PATCH). |
| **Message vs Post** | A **Message** is reusable content (text + assets). A **Post** is a scheduled or published instance tied to one or more social profiles. |
| **IDs** | All resource IDs are strings, and most carry a type prefix -- messages `005`, social profiles `003-`, workflows `cwf`, custom calendar events `0CE`. |
| **Errors** | Non-2xx responses return `{ error: string, statusCode: number }`. |

---

## Campaigns

### `list_campaigns`

List campaigns from Oktopost API with optional filters such as search term, status, and whether
to include tags. Supports pagination (_page, _count) and ordering (_order). Use _order for the
sort field and _orderDirection (asc/desc) to set direction. Campaign IDs are needed by
create_message, create_board_story, and list_posts.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `q` | string |  | Search term to filter campaigns |
| `status` | string |  | Filter by campaign status. One of: `active`, `complete`, `paused`, `archived`. |
| `withTags` | boolean |  | Include campaign tags in the response Defaults to `False`. |
| `_page` | integer |  | Page number (zero-indexed, default: 0) |
| `_count` | integer |  | Results per page (default: 15, max: 200) |
| `_order` | string |  | Sort field (default: created). Direction is set separately via _orderDirection. One of: `created`, `name`, `status`. |
| `_orderDirection` | string |  | Sort direction for _order (default: desc). One of: `asc`, `desc`. |

**Returns:** Array of campaign objects (`id`, `name`, `createdAt`, `updatedAt`, `status`, optional `stats`).

### `get_campaign_by_id`

Get a single campaign by its ID, optionally including campaign tags. Get campaignId from
list_campaigns.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string | * | The ID of the campaign to retrieve |
| `withTags` | boolean |  | Include campaign tags in the response Defaults to `False`. |

**Returns:** Full campaign object with metadata and optional stats.

### `create_campaign`

Create a new campaign with a specified name, optional URL, and tags. Search existing campaigns
with list_campaigns first and follow the account's naming conventions. Use the returned Id with
create_message to add content.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | * | The campaign name. |
| `url` | string |  | The campaign URL. It allows users to insert a URL more quickly when creating posts. |
| `tagIds` | string |  | A comma separated list of Tag Ids. Campaign tags apply to all messages in the campaign unless the user changes them. |

**Returns:** Created campaign object with generated `id`.

### `update_campaign`

Update an existing campaign's name, URL, status, or tags. Status options: active, paused (stops
scheduled posts), archived (deletes scheduled posts). Get campaignId from list_campaigns.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string | * | The ID of the campaign to update |
| `name` | string |  | The new campaign name |
| `url` | string |  | The new campaign URL |
| `status` | string |  | Campaign status. One of: `active`, `paused`, `archived`. |
| `tagIds` | string |  | Comma-separated list of tag IDs |

**Returns:** Updated campaign object.

**Note:** Updating a campaign does not cascade changes to its posts or messages.

### `delete_campaign`

Permanently delete a campaign by ID. This removes the campaign and all its associated data. Get
campaignId from list_campaigns.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string | * | The ID of the campaign to delete |

**Returns:** Confirmation.

---

## Messages

### `list_messages`

List messages in a single campaign or by a list of message IDs. Message IDs are used with
create_post, update_message, and create_board_story.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string |  | The Oktopost campaign Id. Mandatory if 'ids' is not provided. |
| `withTags` | boolean |  | Includes the message tags in the response. Defaults to `False`. |
| `network` | string |  | Filters by the social network: Twitter, LinkedIn, Facebook, Instagram, YouTube, or TikTok. One of: `Twitter`, `LinkedIn`, `Facebook`, `Instagram`, `YouTube`, `TikTok`. |
| `ids` | string |  | Comma separated list of message IDs (start with 005), max 100. Mandatory if 'campaignId' is not provided. |

**Returns:** Array of message objects (`id`, `campaignId`, `body`, `createdAt`, `updatedAt`, optional `tags`, optional `assets`).

### `get_message_by_id`

Retrieve a message's full content (body text, link URL, media attachments) by its messageId
(starts with 005). Messages hold the actual text that posts deliver to social networks. Get
messageId from a Post's MessageId field or from list_messages.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `messageId` | string | * | The ID of the message to retrieve (starts with 005). Typically obtained from a Post's MessageId field or from list_messages. |
| `withTags` | boolean |  | Includes the message tags in the response. Defaults to `False`. |

**Returns:** Full message object.

### `create_message`

Create a new message (the content asset: body text, link, media). Messages are not published
directly — use create_post to schedule delivery to a social profile, or pass the returned Id as
messageIds to create_board_story to add as a shareable variation in an advocacy story. Get
campaignId from list_campaigns and network from list_social_profiles.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `network` | string | * | The social network: Facebook, Twitter, LinkedIn, YouTube, Instagram, or TikTok. One of: `Facebook`, `Twitter`, `LinkedIn`, `YouTube`, `Instagram`, `TikTok`. |
| `campaignId` | string | * | The campaign Id for the message. |
| `message` | string | * | The messages' content. |
| `linkUrl` | string |  | Link attachment Url. |
| `linkTitle` | string |  | Link attachment title. |
| `description` | string |  | Link attachment description. |
| `imageUrl` | string |  | Link attachment image Url. |
| `tagIds` | string |  | A list of comma separated tag Ids. If empty, the message will inherit tags from the campaign. |
| `media` | string |  | The media attachment Id (from create_media or list_media). |
| `title` | string |  | The title for YouTube videos. |

**Returns:** Created message object with generated `id`.

### `update_message`

Update a message's text content, link attachment fields (linkUrl, linkTitle, description,
imageUrl), media, tags, or YouTube title. All link attachment fields must be provided together
when updating link attachments.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `messageId` | string | * | The ID of the message to update (starts with 005) |
| `message` | string |  | Updated message content |
| `linkUrl` | string |  | Link attachment URL |
| `linkTitle` | string |  | Link attachment title |
| `description` | string |  | Link attachment description |
| `imageUrl` | string |  | Link attachment image URL |
| `tagIds` | string |  | Comma-separated list of tag IDs |
| `media` | string |  | Media attachment ID |
| `title` | string |  | Title for YouTube videos |

**Returns:** Updated message object.

### `delete_message`

Permanently delete a message by ID. Any posts created from this message are not affected. Get
messageId from list_messages.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `messageId` | string | * | The ID of the message to delete (starts with 005) |

**Returns:** Confirmation.

---

## Posts

### `list_posts`

List posts with optional filters: campaignId, messageId, status, createdBy, source, date range
(before/after). Supports pagination (_page, _count) and ordering (_order: created, modified,
startDateTime). LinkedIn posts may include Post.FirstComment (comment text and optional image).
Post IDs are used with get_post, update_post, delete_post, and process_workflow_item.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `campaignId` | string |  | Filter by campaign ID |
| `messageId` | string |  | Filter by message ID (starts with 005) |
| `status` | string |  | Filter by post status. One of: `pending`, `inqueue`, `inqueue-draft`, `draft`, `complete`, `incomplete`, `error`. |
| `createdBy` | string |  | Filter by the user ID who created the post |
| `source` | string |  | Filter by creation source. One of: `UI`, `API`, `Autoposter`, `Bookmarklet`, `Board`, `Embedded`. |
| `before` | string |  | Exclusive end of date range for the _order field. Format: YYYY-MM-DD HH:MM:SS |
| `after` | string |  | Inclusive start of date range for the _order field. Format: YYYY-MM-DD HH:MM:SS |
| `_page` | integer |  | Page number (default: 0) |
| `_count` | integer |  | Results per page (default: 25). One of: `25`, `50`, `100`. |
| `_order` | string |  | Sort order field (default: created). One of: `created`, `modified`, `startDateTime`. |

**Returns:** Array of post objects (`id`, `messageId`, `campaignId`, `profileId`, `scheduledAt`, `status`, `body`).

### `get_post`

Retrieve a post's scheduling metadata (status, network, social profile, timestamps) by its
postId (starts with 004). A post does not contain the message text — to get the actual content,
use get_message_by_id with the post's MessageId field. LinkedIn posts may include
Post.FirstComment (comment text and optional image); unlike message text, that content is
already on the post. Get postId from list_posts or create_post.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | The ID of the post to retrieve (starts with 004). Do not pass a messageId here. |
| `stats` | integer |  | Optional: Set to 1 to include updated stats per social post. One of: `0`, `1`. Defaults to `0`. |

**Returns:** Full post object.

### `create_post`

Schedule a message for delivery to one or more social profiles at a specific date/time. The post
references an existing message by messageId. Get messageId from create_message or list_messages,
and credentialIds from list_social_profiles. For LinkedIn posts, optionally pass firstComment
(text and/or an image media ID). The first comment is published after the LinkedIn post
succeeds; if the post fails, the comment is not published. If credentialIds includes multiple
profiles, firstComment is applied to every LinkedIn profile; non-LinkedIn profiles are created
without a first comment. If no LinkedIn profile is included, the request is rejected.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `messageId` | string | * | The message ID (starts with 005). |
| `credentialIds` | string | * | Comma separated values of social profile IDs. Each ID starts with prefix 003- |
| `startDateTime` | integer |  | Unix timestamp. Scheduled time for the post to go out. |
| `status` | string |  | Post status. One of: `pending`, `draft`. |
| `workflowId` | string |  | The workflow ID (starts with cwf) to add this post to for approval. Post will enter the workflow approval process. |
| `targetingPresetId` | string |  | A targeting preset ID to apply LinkedIn audience targeting. Applies to LinkedIn profiles only. Get IDs from list_targeting_presets. |
| `firstComment` | object |  | First comment published after the LinkedIn post succeeds. LinkedIn only. Must include text and/or an image media ID. Applied to every LinkedIn profile in credentialIds; non-LinkedIn profiles are created without a first comment. The request is rejected if no LinkedIn profile is included. Omit to create the post without a first comment. |
| `firstComment.text` | string |  | Comment text. Max 3000 characters. Text is trimmed; it may be empty after trimming only when media is provided. |
| `firstComment.media` | string |  | A single pre-uploaded image media ID from create_media or list_media. Videos and PDFs are rejected. On update_post, pass an empty string to remove attached media. |

**Returns:** Created post object with generated `id`.

**Note:** `credentialIds` is a comma-separated string and may name several profiles at once -- one call schedules the same message across all of them. `firstComment` is LinkedIn-only and the call is rejected if no LinkedIn profile is included.

### `update_post`

Update an existing social media post. Only posts that have not yet been sent can be updated. For
unsent LinkedIn posts, firstComment can be added, partially updated, or removed. Pass null or an
empty object to remove the entire first comment; pass {"media": ""} to remove only the attached
image and preserve the text. Omit firstComment to leave it unchanged. Get postId from
list_posts.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | The ID of the post to update (starts with 004). |
| `messageId` | string |  | The message ID (starts with 005). |
| `credentialIds` | string |  | Comma separated values of social profile IDs. |
| `startDateTime` | integer |  | Unix timestamp. Scheduled time for the post to go out. |
| `status` | string |  | Post status. One of: `pending`, `draft`. |
| `targetingPresetId` | string |  | A targeting preset ID to apply LinkedIn audience targeting. Applies to LinkedIn profiles only. Get IDs from list_targeting_presets. |
| `firstComment` | string |  | First comment on an unsent LinkedIn post. Omit to leave the existing comment unchanged. Pass null or an empty object to remove the entire first comment. Pass {"media": ""} to remove only the attached image and preserve the text. Send only changed fields for a partial update. |

**Returns:** Updated post object.

**Note:** Published posts cannot be updated -- only deleted.

### `list_social_posts`

List social post delivery log entries (sent/failed) for a given postId. Returns the actual
network-level delivery records for a scheduled post. Get postId from list_posts.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | The ID of the post to retrieve social posts for (starts with 004). |

**Returns:** Array of social post objects with optional stats (impressions, clicks, likes, shares, comments).

### `get_social_post`

Retrieve a single social post (delivery log entry) by its postlogId (starts with 007). Social
posts represent actual sent/failed delivery attempts — NOT the message content. To get a post's
text content, use get_message_by_id instead. Get postlogId from list_social_posts.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postlogId` | string | * | The ID of the social post/delivery log entry (starts with 007). Do not pass a postId (004) or messageId (005) here. |
| `stats` | integer |  | Optional: Set to 1 to include updated stats per social post. One of: `0`, `1`. Defaults to `0`. |

**Returns:** Full social post object with engagement data.

### `get_post_analytics`

Retrieve performance analytics for an individual post including impressions, engagements, and
conversions. A stat value of -1 means the metric is unavailable for that social network. This is
the preferred way to retrieve performance metrics for a single post. Get postId from list_posts.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | The ID of the post to retrieve analytics for (starts with 004). |

**Returns:** Analytics object (impressions, clicks, conversions, likes, comments, shares).

**Note:** Stats for freshly-published posts can lag by up to 24 hours depending on the source network.

### `change_post_campaign`

Move a post to a different campaign. Cannot move posts with RUNNING status. If the post is in a
workflow, only the current step's assigned approver can perform this action. Get postId from
list_posts and campaignId from list_campaigns.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | The ID of the post to move (starts with 004) |
| `campaignId` | string | * | The target campaign ID to move the post to |

**Returns:** Updated post object.

### `delete_post`

Delete a scheduled post by ID. Only posts that have not yet been published can be deleted.
Already-sent posts cannot be removed via the API. Get postId from list_posts.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `postId` | string | * | The ID of the post to delete (starts with 004) |

**Returns:** Confirmation.

**Note:** Deleting a published post removes it from Oktopost's records but does not retract the already-published social post on the network. Deletion on the network must be done manually where the platform allows.

---

## Media and uploads

### `list_media`

List account media assets with optional search, type, and folder filters. Media IDs are used in
create_message, create_board_story, and as firstComment.media on create_post/update_post
(LinkedIn first comments; images only). Use folderId to filter by folder (get folder IDs from
list_media_folders).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `q` | string |  | The file name that you want to search for. |
| `type` | string |  | Filter by media type. One of: `Image`, `Video`, `ImageUrl`, `PDF`. |
| `folderId` | string |  | Filter by folder ID. Pass a folder ID to get media in that folder, pass empty string to get root-level media only, or omit to get all media. |

**Returns:** Array of media objects (`id`, `url`, `type`, `filename`, `createdAt`).

**Note:** Pass `folderId` as an empty string to get root-level media only; omit it entirely to get all media.

### `get_media`

Get a single media object by its ID. Get mediaId from list_media or create_media.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `mediaId` | string | * | The ID of the media to retrieve. |

**Returns:** Full media object.

### `create_media`

Create a new media asset from a valid, publicly accessible image URL. Returns a mediaId usable
in create_message (media field), create_board_story (mediaIds), or as firstComment.media on
create_post/update_post (LinkedIn first comments; images only). Media can be organized into
folders using list_media_folders and create_media_folder.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `resource` | string | * | The valid image URL that can be publicly accessed. |

**Returns:** Created media object with generated `id`.

### `list_uploads`

List account uploads, with optional filtering by status, source URL, and pagination.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `status` | string |  | Status of the upload, one of pending, failed, complete. One of: `pending`, `failed`, `complete`. |
| `source` | string |  | Url-encoded upload source url. |
| `_page` | integer |  | The current page. Defaults to `0`. |
| `_count` | integer |  | The number of results per page. Defaults to `20`. |

**Returns:** Array of upload objects.

### `get_upload`

Get a single upload by ID. Use after create_upload to check processing status.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `uploadId` | string | * | The ID of the upload to retrieve. |

**Returns:** Full upload object.

### `create_upload`

Create a new media upload request. The source must be a public URL to your file. Poll get_upload
to check processing status. Once complete, the upload produces a mediaId usable in
create_message or create_board_story.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `source` | string | * | A public URL to your file. It must support HEAD and GET requests with a Range header for chunked downloads. |
| `name` | string |  | The file name. |
| `mimeType` | string |  | The mime type of the uploaded file. Supported types: video/mp4, image/gif, image/png, image/jpg, image/jpeg, application/pdf. |

**Returns:** Upload object with a signed upload URL.

### `validate_video_upload`

Validate an uploaded video against each social network's specifications (Facebook, LinkedIn,
Twitter, Instagram, YouTube). Returns per-network validation results with any errors. Accepts a
mediaId. Run after create_upload completes to check network compatibility before using the
media.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `mediaId` | string | * | The media ID of the uploaded video to validate |

**Returns:** Validation result (`valid`, `errors`).

### `list_media_folders`

List media folders with optional filtering by parent folder and search. Use returned folder IDs
with list_media (folderId param) to browse media in a folder, or with create_media_folder
(parentFolderId) to nest folders.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `folderId` | string |  | Filter by parent folder ID to list only its direct children. |
| `q` | string |  | Search folders by name. |
| `_count` | integer |  | Maximum number of results to return. |
| `_start` | integer |  | Offset for pagination. |
| `_sortBy` | string |  | Field to sort results by. |
| `_order` | string |  | Sort order. One of: `asc`, `desc`. |

### `get_media_folder`

Get a single media folder by its ID. Get folderId from list_media_folders.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `folderId` | string | * | The ID of the folder to retrieve. |

### `create_media_folder`

Create a new media folder. Use parentFolderId to nest it inside an existing folder, or omit to
create at root level. Get parent folder IDs from list_media_folders.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | * | The name of the new folder. |
| `parentFolderId` | string |  | Parent folder ID to nest this folder under. Omit to create at root level. |

### `rename_media_folder`

Rename an existing media folder. Get folderId from list_media_folders.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `folderId` | string | * | The ID of the folder to rename. |
| `name` | string | * | The new name for the folder. |

### `delete_media_folder`

Permanently delete a media folder by its ID. This cascades to all child folders and media assets
within them. Get folderId from list_media_folders.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `folderId` | string | * | The ID of the folder to delete. |

**Note:** This cascades. Deleting a folder permanently deletes every child folder and every media asset inside them.

---

## Calendar

### `get_calendar`

Retrieve calendar data including campaigns, credentials, media, messages, custom events, and
posts within a specified date range, with optional filters.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `fromDate` | string | * | Start date for the calendar data. Format: YYYY-MM-DD. |
| `toDate` | string | * | End date for the calendar data. Format: YYYY-MM-DD. |
| `filters` | string |  | JSON string of filters (e.g., {"campaigns": ["002000000000001"], "networks": ["LinkedIn"]}). Can include: campaigns, credentials, messages, networks (Facebook, Twitter, LinkedIn, Instagram, YouTube, TikTok), postSources, statuses, users. |

**Returns:** Array of scheduled and published posts within the date range.

### `create_custom_calendar_event`

Create a custom calendar event (milestones, meetings, launches, deadlines, reminders). When
endDate is omitted, a single-day event is created. Get campaign IDs from list_campaigns.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `title` | string | * | Event title. Maximum 80 characters. |
| `description` | string |  | Event description. Maximum 2,000 characters, excluding HTML tags. Defaults to empty. |
| `startDate` | integer | * | Event start date and time as a Unix timestamp. |
| `endDate` | integer |  | Event end date and time as a Unix timestamp. When omitted, a single-day event is created. |
| `campaignIds` | string[] |  | Array of campaign IDs associated with the event. Get IDs from list_campaigns. Defaults to empty. |

### `get_custom_calendar_event`

Retrieve a single custom calendar event by ID. Returns 404 when the event does not exist or the
authenticated user does not have access. Use list_custom_calendar_events to find event IDs.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | * | The custom calendar event ID (starts with 0CE). |

### `list_custom_calendar_events`

List custom calendar events visible to the authenticated user. When no campaign IDs are
provided, all accessible events are returned. Event IDs are used with get_custom_calendar_event,
update_custom_calendar_event, and delete_custom_calendar_event.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ids` | string[] |  | Array of custom calendar event IDs (starts with 0CE). Defaults to all events. |
| `campaignIds` | string[] |  | Array of campaign IDs to filter by. Get IDs from list_campaigns. Defaults to all accessible campaigns. |
| `after` | integer |  | Beginning of the requested date range as a Unix timestamp. |
| `before` | integer |  | End of the requested date range as a Unix timestamp. |
| `_page` | integer |  | Page number (default: 0). |
| `_count` | integer |  | Events per page (default: 25). One of: `25`, `50`, `100`. |
| `_order` | string |  | Sort field (default: created). One of: `created`, `modified`, `startDateTime`. |

### `update_custom_calendar_event`

Update an existing custom calendar event. Only id is required; omitted properties keep their
current values. Get event IDs from list_custom_calendar_events.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | * | The custom calendar event ID (starts with 0CE). |
| `title` | string |  | Event title. Maximum 80 characters. Defaults to current value. |
| `description` | string |  | Event description. Maximum 2,000 characters, excluding HTML tags. Defaults to current value. |
| `startDate` | integer |  | Event start date and time as a Unix timestamp. Defaults to current value. |
| `endDate` | integer |  | Event end date and time as a Unix timestamp. Defaults to current value. |
| `campaignIds` | string[] |  | Array of campaign IDs associated with the event. Get IDs from list_campaigns. Pass an empty array to clear all campaigns. Defaults to current value when omitted. |

### `delete_custom_calendar_event`

Delete a custom calendar event by ID. Returns 404 when the event does not exist, or 403 when the
authenticated user lacks permission. Get event IDs from list_custom_calendar_events.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | * | The custom calendar event ID (starts with 0CE). |

---

## Tags and targeting

### `list_tags`

List publishing tags from Oktopost. Tag IDs can be used by create_message, create_campaign,
update_campaign, update_message, create_board_story, and update_board_story.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `_page` | integer |  | Page number for pagination. |
| `_count` | integer |  | Number of items to return per page. |

### `list_targeting_presets`

List available LinkedIn audience targeting presets for a social profile. Use the returned preset
IDs with create_post or update_post to apply audience targeting. Get credentialId from
list_social_profiles (LinkedIn profiles only).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `credentialId` | string | * | The LinkedIn social profile ID (starts with 003-). |

---

## Social profiles

### `list_social_profiles`

List social profiles, with optional filtering by network and inclusion of invalid credentials.
Profile IDs (credentialIds) are required by create_post to specify which social account to
publish to.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `network` | string |  | Optional: Filter by social network. Acceptable values: LinkedIn, Twitter, YouTube, Instagram, Facebook, WeChat, Xing, TikTok. One of: `LinkedIn`, `Twitter`, `YouTube`, `Instagram`, `Facebook`, `WeChat`, `Xing`, `TikTok`. |
| `includeInvalid` | integer |  | Optional: If set to 1, the response will include invalid credentials. One of: `0`, `1`. Defaults to `0`. |

**Returns:** Array of profile objects (`id`, `name`, `network`, `type`, `imageUrl`, `status`).

### `get_social_profile`

Get a single social profile by its ID. Get profileId from list_social_profiles.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `profileId` | string | * | The ID of the social profile to retrieve (starts with 003-). |

**Returns:** Full profile object.

---

## Approvals and workflows

### `list_workflows`

List all workflows in your account. By default includes all workflow steps and approvers.
Workflow IDs are used with create_post, send_to_workflow, and create_board_story.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `withSteps` | integer |  | Set to 1 to include workflow steps in the response. Defaults to 1. One of: `0`, `1`. |

**Returns:** Array of workflow objects (`id`, `name`, `steps`).

### `get_workflow`

Retrieve a single workflow by ID. Optionally set withSteps to include all approval steps and
their assigned approvers. Get workflowId from list_workflows.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `workflowId` | string | * | The ID of the workflow to retrieve (starts with cwf) |
| `withSteps` | integer |  | Set to 1 to include workflow steps in the response. One of: `0`, `1`. Defaults to `0`. |

**Returns:** Full workflow object with step definitions.

### `list_workflow_items`

List posts, messages, and stories in your workflows that are pending approval. Use
process_workflow_item to approve/reject, or add_workflow_item_note to comment.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `page` | integer |  | The current page (default: 0) |
| `count` | integer |  | The number of results per page. From 1 to 1000 maximum (default: 20) |
| `stepId` | string |  | Return the items in this step only (starts with cws) |
| `workflowId` | string |  | Return the items in this workflow only (starts with cwf) |
| `withHistory` | boolean |  | If set to true, return the history information for each item Defaults to `False`. |
| `withAuthors` | boolean |  | If set to true, return all users present in the CreatedBy field Defaults to `False`. |
| `withSteps` | boolean |  | If set to true, all steps for the requested items are added to the response Defaults to `False`. |

**Returns:** Array of workflow item objects (`id`, `status`, `postId`, `currentStep`).

### `process_workflow_item`

Approve or reject a post, message, or story in the workflow. You can include a note with your
approval/rejection in a single call. Get the entityId (postId, messageId, or storyId) from
list_workflow_items.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `entityId` | string | * | A post (starts with 004), message (starts with 005), or story (starts with 0AS) ID |
| `isApprove` | boolean |  | Set to true to approve, false to reject Defaults to `True`. |
| `note` | string |  | Optional note to include with the approval/rejection |
| `stepId` | string |  | The step ID (starts with cws). If set, it must equal the current item's step in the approval process. Helps avoid potential mistakes when calling this endpoint multiple times |

**Returns:** Updated workflow item.

### `list_workflow_item_notes`

List all notes for a post, message, or story in the approval workflow. Get the entityId (postId,
messageId, or storyId) from list_workflow_items.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `entityId` | string | * | A post (starts with 004), message (starts with 005), or story (starts with 0AS) ID |

**Returns:** Array of note objects.

### `add_workflow_item_note`

Add a note to a post, message, or story in the approval workflow. Provide the entityId (postId,
messageId, or storyId) along with the note text. Get the entityId from list_workflow_items.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `entityId` | string | * | A post (starts with 004), message (starts with 005), or story (starts with 0AS) ID |
| `note` | string | * | The note text to add |

**Returns:** Created note object.

### `send_to_workflow`

Submit a post, message, or story for approval by sending it into a workflow. Requires the
entityId and the target workflowId. The item enters the first approval step. Get workflowId from
list_workflows.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `entityId` | string | * | A post (starts with 004), message (starts with 005), or story (starts with 0AS) ID to submit for approval |
| `workflowId` | string | * | The target workflow ID (starts with cwf) |

**Returns:** Created workflow item.

### `remove_from_workflow`

Remove a post, message, or story from the approval workflow, reverting it to Draft status.
Requires the entityId (post, message, or story ID).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `entityId` | string | * | A post (starts with 004), message (starts with 005), or story (starts with 0AS) ID to remove from the workflow |

**Returns:** Confirmation of removal.

---

## Employee advocacy

#### `list_boards`

List all employee advocacy boards in your Oktopost account. Boards are platforms where advocates
can share posts on their social media channels. Use the returned board Id with
list_board_stories, list_board_topics, get_board, or invite_advocate.

Takes no parameters.

**Returns:** Array of board objects (`id`, `name`, `description`).

#### `get_board`

Retrieve a single advocacy board by ID, including its full configuration (color, expiration,
notifications, leaderboard, signup settings). Get boardId from list_boards.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string | * | The ID of the board to retrieve (starts with brd) |

**Returns:** Full board object.

#### `list_board_topics`

List topics for advocacy boards. Topics allow advocates to filter messages thematically.
Optionally filter by board or search by name. Check existing topics before creating new ones
with create_board_topic. IMPORTANT: If a board has topics, topicIds are required when creating
stories via create_board_story.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string |  | Filter topics by board ID (starts with brd) |
| `q` | string |  | Search for topics by name |

**Returns:** Array of topic objects.

#### `create_board_topic`

Create a new topic for an advocacy board. Topics allow advocates to filter and subscribe to
content thematically. Note: Advocates will see a notification to subscribe to new topics. First
check for existing topics with list_board_topics. Get boardId from list_boards.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string | * | The board ID where the topic will be created (starts with brd) |
| `name` | string | * | The topic name |

**Returns:** Created topic object.

#### `update_board_topic`

Rename an existing board topic. Provide the topicId and the new name. Get topicId from
list_board_topics.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `topicId` | string | * | The ID of the topic to update (starts with tpc) |
| `name` | string | * | The new topic name |

**Returns:** Updated topic object.

#### `list_board_stories`

List stories in an advocacy board. Stories are articles or media assets shared with advocates.
Requires boardId. Use create_board_story to add new stories. Each story's Id can be passed to
get_board_story, update_board_story, or send_to_workflow.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string | * | The board ID to list stories from (starts with brd) |

**Returns:** Array of story objects (`id`, `boardId`, `title`, `body`, `url`, `createdAt`).

#### `get_board_story`

Retrieve a single advocacy story by ID, including its messages, media, topics, and tags. Get
storyId from list_board_stories.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `storyId` | string | * | The ID of the story to retrieve (starts with 0AS) |

**Returns:** Full story object.

#### `create_board_story`

Create a new story in an advocacy board. Stories are articles or media assets that advocates can
share on their social channels. Search for an existing campaign with list_campaigns first. Get
boardId from list_boards. To attach pre-written social messages, create them first with
create_message, then pass their IDs as messageIds. To create a repost story from a LinkedIn
post, pass postlogId — title and description will be auto-derived and link/mediaIds/messageIds
are ignored. Use generateMessages with reposts to auto-create advocate messages. IMPORTANT:
Before creating a story, call list_board_topics with the boardId. If the board has existing
topics, topicIds is REQUIRED and must be a subset of the board's topics (otherwise the API
returns 400). If the board has no topics, topicIds can be omitted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string | * | The board ID where the story will be created (starts with brd) |
| `title` | string |  | The story title. Required unless postlogId is set (auto-derived for reposts). |
| `description` | string |  | The story description. Required unless postlogId is set (auto-derived for reposts). |
| `campaignId` | string | * | The campaign ID to associate with this story |
| `postlogId` | string |  | A LinkedIn postlog ID to create a repost story (type: post-attachment). When set, title and description become optional (auto-derived), and link/mediaIds/messageIds are ignored. |
| `mediaIds` | string |  | Comma-separated media IDs to attach |
| `link` | string |  | Link URL associated with the story |
| `messageIds` | string |  | Comma-separated message IDs (start with 005) for pre-written social post variations that advocates can share. Create messages first with create_message, then pass their IDs here. |
| `topicIds` | string |  | Comma-separated topic IDs (start with tpc). REQUIRED if the board has existing topics (must be a subset; omitting causes a 400 error). Call list_board_topics with the boardId first to check. Omit only if the board has no topics. |
| `tagIds` | string |  | Comma-separated tag IDs |
| `publishDatetime` | number |  | Unix timestamp for when to publish. Defaults to now |
| `expirationDatetime` | number |  | Unix timestamp for expiration. Defaults to board's default expiration |
| `isDraft` | boolean |  | Save as draft. Defaults to false |
| `isFeatured` | boolean |  | Mark as featured. Defaults to false |
| `workflowId` | string |  | Send to approval workflow (starts with cwf) |
| `generateMessages` | boolean |  | Automatically generate messages for this story. Defaults to false |

**Returns:** Created story object.

#### `update_board_story`

Update an existing story in an advocacy board. You can modify title, description, topics,
featured status, and other properties. For repost stories (created with postlogId), the repost
association is preserved on update and title/description can be overridden. Get storyId from
list_board_stories.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `storyId` | string | * | The story ID to update (starts with 0AS) |
| `boardId` | string |  | The board ID (starts with brd) |
| `title` | string |  | Updated story title |
| `description` | string |  | Updated story description |
| `campaignId` | string |  | Updated campaign ID |
| `mediaIds` | string |  | Comma-separated media IDs to attach |
| `link` | string |  | Updated link URL |
| `messageIds` | string |  | Comma-separated message IDs (start with 005) for pre-written social post variations that advocates can share. Create messages with create_message, then pass their IDs here. |
| `topicIds` | string |  | Comma-separated topic IDs (start with tpc) |
| `tagIds` | string |  | Comma-separated tag IDs |
| `publishDatetime` | number |  | Unix timestamp for when to publish |
| `expirationDatetime` | number |  | Unix timestamp for expiration |
| `isDraft` | boolean |  | Update draft status |
| `isFeatured` | boolean |  | Update featured status |
| `workflowId` | string |  | Send to approval workflow (starts with cwf) |
| `generateMessages` | boolean |  | Automatically generate messages for this story |

**Returns:** Updated story object.

#### `delete_board_story`

Permanently delete a story from an advocacy board by its ID. Get storyId from
list_board_stories.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `storyId` | string | * | The ID of the story to delete (starts with 0AS) |

**Returns:** Confirmation.

#### `delete_board_topic`

Permanently delete a topic from an advocacy board. Advocates subscribed to this topic will no
longer see it. Get topicId from list_board_topics.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `topicId` | string | * | The ID of the topic to delete (starts with tpc) |

**Returns:** Confirmation.

#### `list_advocates`

List advocates in your account. Optionally scope to a board (boardId) for extended fields and
activity filters. Supports pagination. Returns advocate IDs usable with get_advocate,
delete_advocate, and invite_advocate (pass Id as userId to re-invite).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string |  | Scope results to a specific board. Enables activity filters (lastSeen, notSeen, neverSeen) and additional response fields (Shares, LastSeen, Role, RoleId, CustomFields, Leaderboards). |
| `email` | string |  | Filter by exact email address |
| `lastSeen` | integer |  | Return advocates seen within the last N days. Requires boardId. |
| `notSeen` | integer |  | Return advocates NOT seen within the last N days. Requires boardId. |
| `neverSeen` | boolean |  | Return advocates who have never logged in to the board. Requires boardId. |
| `_page` | integer |  | Page number (default: 0) |
| `_count` | integer |  | Results per page (default: 25). One of: `25`, `50`, `100`. |

**Returns:** Array of advocate objects (`id`, `name`, `email`, `status`).

#### `get_advocate`

Retrieve a single advocate by ID. Optionally pass boardId to include the advocate's subscribed
topics and latest shares for that board. Get advocateId from list_advocates.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `advocateId` | string | * | The ID of the advocate to retrieve (starts with 00A) |
| `boardId` | string |  | Board ID (starts with brd). If provided, includes Topics and LatestShares for that board |

**Returns:** Full advocate object.

#### `invite_advocate`

Invite advocates to an advocacy board, or re-invite existing ones. Requires boardId from
list_boards. New invite: firstName, lastName, and email. Re-invite: userId from list_advocates
(use neverSeen/notSeen to find advocates who have never logged in or have not been active
recently). For one person, pass those fields at the top level. For several, pass users (1-100
entries; new invites and re-invites can be mixed). Do not send top-level person fields together
with users. Optional message is a note on the invitation email, applied to every entry in the
request. Bulk invites may partially succeed: valid entries are invited and invalid ones are
listed in Errors.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `boardId` | string | * | The board ID to invite advocates to (starts with brd). |
| `firstName` | string |  | Single new invite only. Required with lastName and email. Do not send with users or userId. |
| `lastName` | string |  | Single new invite only. Required with firstName and email. Do not send with users or userId. |
| `email` | string |  | Single new invite only. Required with firstName and lastName. Do not send with users or userId. |
| `userId` | string |  | Single re-invite only. Advocate/user ID (starts with 00A) from list_advocates. Do not send with users or with firstName/lastName/email. |
| `users` | object[] |  | Bulk invite (POST /v2/advocate/bulk). Array of 1-100 entries. Each entry is a new invite (firstName, lastName, email) or a re-invite (userId). Do not send top-level firstName, lastName, email, or userId when using users. |
| `message` | string |  | Personal note attached to the invitation email. Applied to every invite in this request, including re-invites. Max 1024 characters. |

**Returns:** Created advocate invitation.

#### `delete_advocate`

Remove an advocate from a specific board. Requires both advocateId and boardId since an advocate
can belong to multiple boards. Get advocateId from list_advocates and boardId from list_boards.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `advocateId` | string | * | The ID of the advocate to remove (starts with 00A) |
| `boardId` | string | * | The board ID to remove the advocate from (starts with brd) |

**Returns:** Confirmation.

---

## Users

### `list_users`

List users in the platform with basic information including name, email, role, and last login.
Supports name search (q), pagination (_page, _count), and ordering (_order). Use _order for the
sort field and _orderDirection (asc/desc) to set direction. User IDs appear in createdBy fields
on posts and messages.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `q` | string |  | Filter users by name (partial match) |
| `_page` | integer |  | Page number (zero-indexed, default: 0) |
| `_count` | integer |  | Results per page (default: 25). One of: `25`, `50`, `100`. |
| `_order` | string |  | Sort field. Direction is set separately via _orderDirection. One of: `name`, `email`. |
| `_orderDirection` | string |  | Sort direction for _order (default: asc). One of: `asc`, `desc`. |

**Returns:** Array of user objects (`id`, `name`, `email`, `role`).

### `get_user`

Get a single user by their ID with detailed information including profile data and social media
connections. Get userId from list_users.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `userId` | string | * | The ID of the user to retrieve |

**Returns:** Full user object.

---

## Social BI (added in v2.8.0)

### `list_dashboards`

List Social BI dashboards accessible to the authenticated user. Returns a paginated list of
dashboards with metadata. Use get_dashboard to retrieve a specific dashboard and its report
widgets.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `_page` | integer |  | Page number (0-based) Defaults to `0`. |
| `_count` | integer |  | Results per page Defaults to `25`. |
| `_order` | string |  | Sort field and direction. Format: 'field,direction' where direction is 0 (desc) or 1 (asc). Fields: name, description, visibility, createdBy, creatorName, createdOn. Defaults to `created,0`. |
| `search` | string |  | Filter by dashboard name (substring match) |
| `visibility` | string |  | Filter by dashboard visibility. One of: `shared`, `private`. |

**Returns:** Array of dashboard objects (`id`, `name`).

### `get_dashboard`

Get a single Social BI dashboard by ID, including its list of report widgets. Use the widget IDs
with get_dashboard_report_data to fetch computed analytics data. Get dashboardId from
list_dashboards.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dashboardId` | string | * | The ID of the dashboard to retrieve |

**Returns:** Full dashboard object with widget definitions.

### `get_dashboard_report_data`

Execute a report widget query within a Social BI dashboard and return the computed analytics
data. The report runs using the dashboard's date range and filters. Get dashboardId from
list_dashboards and reportId (widget ID) from get_dashboard.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dashboardId` | string | * | The ID of the dashboard containing the report |
| `reportId` | string | * | The widget/report ID to query (from the dashboard's Widgets list) |
| `filter` | object |  | Additional filter criteria (JSON object) |

**Returns:** Report data matching the widget configuration (metrics, dimensions, time series).

---

## Inbox (added in v2.7.0)

### `list_conversations`

List inbox items (direct messages, post comments, mentions, and replies) from connected social
profiles. Supports filtering by type, status, network, assignee, tag, and free-text search. Use
the returned Id with get_conversation, get_conversation_timeline, reply_to_conversation,
assign_conversation, or update_conversation_status.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `type` | string |  | Comma-separated item types. Accepted: Conversation (direct message), Post (comment on your post), Mention, Reply. Defaults to all. |
| `status` | string |  | Comma-separated statuses. Accepted: open, closed |
| `network` | string |  | Comma-separated networks. Accepted: Facebook, Twitter, LinkedIn, YouTube, Instagram, TikTok. One of: `Facebook`, `Twitter`, `LinkedIn`, `YouTube`, `Instagram`, `TikTok`. |
| `assignee_id` | string |  | Comma-separated user IDs to filter by assignee. Get IDs from list_users. |
| `tag` | string |  | Comma-separated conversation tag names to filter by. Get names from list_conversation_tags. |
| `q` | string |  | Free-text search term. |
| `_count` | integer |  | Maximum number of results to return. |

**Returns:** Array of conversation objects.

### `get_conversation`

Retrieve a single inbox item by ID, including its assigned tags. Get conversationId from
list_conversations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | The inbox item ID (starts with eit). |

**Returns:** Full conversation object.

### `get_conversation_timeline`

Retrieve the timeline of an inbox item, including messages, comments, notes, shares, and likes.
Supports cursor-based pagination via last_loaded_id (not _page/_count). Get conversationId from
list_conversations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | The inbox item ID (starts with eit). |
| `last_loaded_id` | string |  | The ID of the last loaded timeline entry for cursor-based pagination to load older entries. |

**Returns:** Ordered array of timeline events (messages, assignments, status changes).

### `reply_to_conversation`

Send a reply or comment on an inbox item. For Conversation type items this sends a DM; for
Post/Mention/Reply types this adds a public comment. The item must be in open status — use
update_conversation_status to reopen if needed. Supports threading via parent_comment_id on
Facebook, LinkedIn, Instagram, TikTok, and YouTube. Get conversationId from list_conversations.
Use list_canned_responses to find reusable reply templates.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | The inbox item ID (starts with eit). |
| `message` | string | * | The reply text (max 10,000 characters). |
| `parent_comment_id` | string |  | Parent comment ID for threading on public items. Supported on Facebook, LinkedIn, Instagram, TikTok, and YouTube. Ignored for direct messages. |

**Returns:** Created reply object.

### `assign_conversation`

Assign an inbox item to a user. Optionally include a note that will also be added to the item's
timeline. Get conversationId from list_conversations and assignee_id from list_users.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | The inbox item ID (starts with eit). |
| `assignee_id` | string | * | The user ID to assign the conversation to. Get from list_users. |
| `note` | string |  | A note to attach with the assignment (max 10,000 characters). |

**Returns:** Updated conversation object.

### `update_conversation_status`

Open or close an inbox item. Get conversationId from list_conversations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | The inbox item ID (starts with eit). |
| `status` | string | * | The new status. One of: `open`, `closed`. |

**Returns:** Updated conversation object.

### `add_conversation_note`

Add an internal note to an inbox item's timeline. Get conversationId from list_conversations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | The inbox item ID (starts with eit). |
| `note` | string | * | The note text (max 10,000 characters). |

**Returns:** Created note object.

#### `list_conversation_tags`

List all conversation tags for the account. Use the returned tag names with
update_conversation_tags.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `q` | string |  | Search term to filter tags by name. |
| `_page` | integer |  | Page number for pagination. |
| `_count` | integer |  | Number of results per page (max 20). |
| `_order` | string |  | Sort field and direction, e.g. name,1 for ascending by name. |

**Returns:** Array of tag objects (`id`, `name`, `color`).

#### `get_conversation_tag`

Retrieve a single conversation tag by ID. Get tagId from list_conversation_tags.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tagId` | string | * | The conversation tag ID (starts with etg). |

**Returns:** Full tag object.

#### `update_conversation_tag`

Rename an existing conversation tag. Get tagId from list_conversation_tags.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tagId` | string | * | The conversation tag ID (starts with etg). |
| `tag` | string | * | The new tag name (max 64 characters). |

**Returns:** Updated tag object.

#### `update_conversation_tags`

Replace the tags assigned to an inbox item. IMPORTANT: This replaces ALL tags — any previously
assigned tags not in the list will be removed. Call get_conversation first to see current tags,
then include any existing tags you want to keep. Get available tag names from
list_conversation_tags. Get conversationId from list_conversations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | The inbox item ID (starts with eit). |
| `tags` | string[] | * | Array of conversation tag names to assign. Replaces all existing tags. |

**Returns:** Updated conversation object.

#### `delete_conversation_tag`

Delete a conversation tag. The tag will be removed from all conversations it was assigned to.
Get tagId from list_conversation_tags.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tagId` | string | * | The conversation tag ID to delete (starts with etg). |

**Returns:** Confirmation.

#### `list_canned_responses`

List reusable reply templates for inbox conversations. Use the returned content with
reply_to_conversation for consistent replies.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `q` | string |  | Search term to filter by name. |
| `_page` | integer |  | Page number for pagination. |
| `_count` | integer |  | Number of results per page. |
| `_order` | string |  | Sort field and direction, e.g. created,0 for descending by creation date. |

**Returns:** Array of canned response objects (`id`, `title`, `body`).

#### `get_canned_response`

Retrieve a single canned response by ID. Get cannedResponseId from list_canned_responses.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cannedResponseId` | string | * | The canned response ID (starts with cnr). |

**Returns:** Full canned response object.

#### `create_canned_response`

Create a new reusable reply template for inbox conversations. Returns 409 if a canned response
with the same name already exists.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | * | The display name (max 64 characters). Must be unique. |
| `content` | string | * | The response body text (max 10,000 characters). |
| `visibility` | string |  | Who can see this response. Defaults to shared. One of: `shared`, `private`. |

**Returns:** Created canned response object.

#### `create_salesforce_case`

Create or update a Salesforce case linked to an inbox item. IMPORTANT: Requires an active
Salesforce integration — returns 400 if none is configured. The integration_id must be known in
advance (there is no discovery tool for it). Get conversationId from list_conversations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `conversationId` | string | * | The inbox item ID (starts with eit). |
| `integration_id` | string | * | The Salesforce case integration ID. |
| `case_owner` | string |  | The Salesforce case owner. |
| `contact_id` | string |  | The Salesforce contact ID to associate with the case. |
| `case_description` | string |  | A description for the Salesforce case (max 10,000 characters). |

**Returns:** Created Salesforce case object with external case ID.
---

## What does NOT exist

These tools, parameters, and behaviors are **not available**. Do not hallucinate them.

### Non-existent tools
- **`bulk_publish`** or **`bulk_create`** — Messages must be created individually. Note that a single `create_post` call *can* fan one message out to many profiles via `credentialIds`, so that is not a bulk-tool workaround, it is the supported path.
- **`search_posts`** — There is no dedicated search tool. Filter with the query parameters on `list_posts` (`q`, `status`, `before`, `after`, `createdBy`, `source`).
- **`undo_publish`** — Published posts cannot be unpublished from the source network via API. `delete_post` removes the record from Oktopost but does not retract what's already live.
- **`A/B_test`** — There is no A/B test parameter on posts. A/B testing must be done manually by creating separate posts.
- **`send_feedback`** — Not exposed by the MCP server. Feedback goes through the Oktopost product directly.

### Cascading delete gotchas
- `delete_media_folder` **does** cascade, and it is the only delete that does: it permanently removes every child folder and every media asset inside them.
- `delete_campaign` does NOT cascade. Posts and messages under it become orphaned. If you care about attribution, re-assign posts with `change_post_campaign` first.
- `delete_message` does NOT delete posts created from that message.
- `delete_board_topic` does NOT delete the stories tagged to it — they become untagged.

### Non-existent parameters
- **`numberOfImages`** — Does not exist on any tool.
- **`negativePrompt`** — Does not exist on any tool.
- **`seed`** — No reproducibility seed parameter exists.

### Unsupported behaviors
- **Cursor-based pagination** — Not supported. Pagination is offset-based, but the parameter names vary per tool — see the Pagination row in Global API conventions.
- **Real-time analytics streaming** — Analytics data has daily granularity. There is no live streaming.
- **Direct Instagram Story publishing** — Stories cannot be published via the API.
