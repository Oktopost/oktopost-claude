# Social networks reference

Per-network specifications, character limits, media specs, and B2B best practices for creating and validating social content through Oktopost.

---

## LinkedIn (primary for B2B)

### Character limits
- **Post body:** 3,000 characters
- **Company page name:** 100 characters
- **Comment:** 1,250 characters
- **Link preview headline:** 70 characters (truncates after)
- **Link preview description:** 100 characters (truncates after)

### Media specifications
- **Single image:** 1080x1080 (square) or 1200x627 (landscape link share). JPG/PNG, max 10 MB.
- **Carousel/document:** PDF upload, up to 300 pages, max 100 MB. 1080x1080 or 1920x1080 per slide.
- **Video:** MP4, 3 seconds to 10 minutes, max 5 GB. Recommended 1920x1080.
- **GIF:** supported in posts, max 5 MB.

### Hashtag guidelines
- **Optimal count:** 3-5 per post.
- **Placement:** End of post body, separated by a line break from main text.
- **Mix:** 1-2 broad industry tags + 2-3 niche/branded tags.
- **Avoid:** Hashtag walls, mid-sentence hashtags, trending-only tags with no relevance.

### B2B best practices
- Native document/carousel posts get highest organic reach; PDFs outperform images.
- Company page posts have lower organic reach than personal profiles; pair with employee advocacy.
- Algorithm favors dwell time (long reads), comments over reactions, and expertise/authority signals.
- **Optimal posting:** Tue-Thu, 8-10 AM and 12-1 PM in target audience timezone. 3-5x per week.
- **Avoid:** Excessive emoji, engagement bait ("agree?"), pods/engagement groups, posting external links without context. The "link in first comment" tactic no longer provides a reach advantage.

### API/Oktopost quirks
- Oktopost publishes to company pages and personal profiles via LinkedIn API.
- Document/carousel posts require PDF upload; cannot be composed as native multi-image carousels via API.
- Polls cannot be created via API.
- Mention tagging uses URN format; display names must match exactly.

---

## X/Twitter

### Character limits
- **Post body:** 280 characters (threads for longer content).
- **Quote post:** 280 characters + quoted post.
- **Reply:** 280 characters.
- **DM:** 10,000 characters.

### Media specifications
- **Image:** 1600x900 recommended (16:9). JPG/PNG/GIF. Max 5 MB (images), 15 MB (GIF).
- **Video:** MP4, max 2 minutes 20 seconds, max 512 MB. Recommended 1280x720 or 1920x1080.
- **Up to 4 images** per post, or 1 GIF, or 1 video.

### Hashtag guidelines
- **Optimal count:** 1-2, integrated naturally into the post text.
- **Placement:** Inline within the sentence or at the end.
- **Avoid:** More than 3 hashtags (reduces engagement), hashtag-only posts.

### B2B best practices
- Threads work well for thought leadership and breaking down complex topics.
- Algorithm weights: replies > reposts > likes; media (images/video) boosts reach.
- **Optimal posting:** Weekdays, 9 AM-12 PM in target timezone. 1-3x per day.
- Short, punchy takes with a clear point of view outperform generic announcements.
- **Avoid:** Auto-cross-posting LinkedIn content verbatim (tone mismatch), thread spam.

### API/Oktopost quirks
- Oktopost supports single posts and image attachments.
- Thread publishing requires sequential API calls; Oktopost does not natively compose threads.
- Alt text for images can be set via API and should always be included.

---

## Facebook

### Character limits
- **Post body:** 63,206 characters (but 80-150 characters gets highest engagement).
- **Comment:** 8,000 characters.
- **Link preview headline:** 88 characters (truncates after).
- **Page name:** 75 characters.

### Media specifications
- **Image:** 1200x630 (link share/landscape). JPG/PNG. Max 10 MB.
- **Video:** MP4/MOV, up to 240 minutes, max 10 GB. Recommended 1280x720+.
- **Carousel:** 2-10 cards, 1080x1080 per card.
- **GIF:** supported, max 25 MB.

### Hashtag guidelines
- **Optimal count:** 0-2. Hashtags are mostly irrelevant for Facebook reach.
- **Placement:** End of post if used at all.
- **Avoid:** Hashtag-heavy posts; Facebook's algorithm does not reward them.

### B2B best practices
- Algorithm prioritizes meaningful interactions (comments, shares with commentary) and group content over page content.
- Video (especially live) outperforms image, which outperforms text-only.
- **Optimal posting:** Tue-Thu, 1-4 PM in target timezone. 3-5x per week.
- Facebook is declining for organic B2B but remains relevant for retargeting audiences via Meta Ads and community groups.
- **Avoid:** Engagement bait (Facebook actively demotes it), link-only posts without context.

### API/Oktopost quirks
- Oktopost publishes to Facebook pages (not personal profiles).
- Link previews are auto-generated; custom thumbnails require og:image meta tags on the destination URL.
- Stories and Reels cannot be published via Oktopost/API for pages.

---

## Instagram

### Character limits
- **Caption:** 2,200 characters.
- **Comment:** 2,200 characters.
- **Bio:** 150 characters.
- **Hashtags in caption or first comment:** both approaches work; algorithm treats them equally.

### Media specifications
- **Feed image:** 1080x1080 (square), 1080x1350 (portrait), 1080x566 (landscape). JPG/PNG. Max 8 MB.
- **Story/Reel:** 1080x1920 (9:16). Video max 90 seconds (Reel), 60 seconds (Story).
- **Carousel:** 2-10 slides, 1080x1080 or 1080x1350. All slides must share the same aspect ratio.
- **Video:** MP4, max 60 minutes (feed), 90 seconds (Reel). Max 3.6 GB.

### Hashtag guidelines
- **Optimal count:** 5-15 per post.
- **Placement:** End of caption or first comment (no algorithmic difference).
- **Mix:** Broad + niche + branded. Rotate sets to avoid shadow-ban triggers.
- **Avoid:** Banned/spammy hashtags, using the same 30 hashtags on every post.

### B2B best practices
- Reels get highest organic reach; the algorithm heavily favors short-form video.
- B2B presence is growing but remains secondary to LinkedIn for most industries.
- Employer branding, culture content, and event coverage perform best for B2B.
- **Optimal posting:** Tue-Fri, 10 AM-1 PM in target timezone. 3-5x per week.
- **Avoid:** Hard-sell product posts, link-heavy captions (links are not clickable in captions).

### API/Oktopost quirks
- Oktopost publishes feed posts (single image, carousel, Reels) via Instagram Graph API.
- Stories cannot be published via API; must be posted natively.
- Links in captions are not clickable; use "link in bio" CTA or Linktree-style tools.
- Instagram requires a connected Facebook page for API publishing.

---

## Validation rules

| Check | LinkedIn | X | Facebook | Instagram |
|---|---|---|---|---|
| Body length | <= 3,000 | <= 280 | <= 63,206 | <= 2,200 |
| Hashtag count | 3-5 | 1-2 | 0-2 | 5-15 |
| Image ratio | 1.91:1 or 1:1 | 16:9 | 1.91:1 | 1:1 or 9:16 |
| Video max duration | 10 min | 2:20 | 240 min | 90 sec (Reel) |
| Link in body | Yes | Yes | Yes | No (bio link) |
| Image max size | 10 MB | 5 MB | 10 MB | 8 MB |

## B2B content type performance

| Content type | LinkedIn | X | Facebook | Instagram |
|---|---|---|---|---|
| Thought leadership | HIGH | MED | LOW | LOW |
| Product updates | MED | MED | LOW | MED |
| Employee advocacy | HIGH | MED | MED | MED |
| Industry data/stats | HIGH | HIGH | LOW | MED |
| Event promotion | MED | MED | MED | HIGH |
| Customer stories | HIGH | MED | MED | HIGH |
| Culture/employer brand | MED | LOW | MED | HIGH |
| How-to/educational | HIGH | MED | MED | MED |
