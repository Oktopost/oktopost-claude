# Oktopost Analytics and Metrics Reference

Metrics glossary, B2B benchmarks, interpretation patterns, and reporting templates for Oktopost social analytics.

---

## Metrics Glossary

Every metric returned by the Oktopost API and what it measures:

| Metric | Description |
|---|---|
| `LinkClicks` | Clicks on okt.to tracked links. The primary engagement metric for measuring content-driven traffic. Only counts clicks on Oktopost-shortened URLs. |
| `Conversions` | Conversion pixel fires attributed to a social post. Tracks when a visitor who clicked a social link completes a defined conversion action (form fill, signup, demo request). |
| `Comments` | Total comment count on published posts across all networks. Indicates content that sparks conversation. |
| `Likes` | Reactions and likes across networks. LinkedIn reactions (like, celebrate, insightful, etc.) all count as likes. |
| `Shares` | Reposts, shares, and retweets. The strongest organic amplification signal — someone found the content worth redistributing. |
| `ImpressionsAdded` | Number of times content was displayed in feeds. High impressions with low engagement suggests reach without relevance. |
| `MediaClicksAdded` | Clicks on images, videos, or other media attachments within a post. Distinct from link clicks. |
| `UserFollowsAdded` | New followers gained on the social profile. Tracks audience growth attributable to content activity. |
| `Reach` | Unique accounts that saw the content. Unlike impressions, reach counts each account only once regardless of how many times they saw the post. |
| `DetailExpandsAdded` | "See more" clicks, primarily on LinkedIn. Indicates the hook was strong enough to make someone expand truncated text. |
| `BoardClicks` | Clicks on links shared through advocacy board posts. Tracks employee advocacy traffic separately from company page organic traffic. |
| `BoardConverts` | Conversions attributed to advocacy board shares. The advocacy equivalent of the `Conversions` metric. |

---

## B2B Benchmark Ranges

Performance benchmarks by network. Use these to contextualize results when analyzing campaign performance.

| Metric | LinkedIn (Good / Great) | X (Good / Great) | Facebook (Good / Great) |
|---|---|---|---|
| Engagement Rate | 2-4% / >5% | 0.5-1% / >2% | 0.5-1% / >2% |
| Click-Through Rate | 0.8-1.5% / >2% | 0.5-1% / >1.5% | 0.5-1% / >1.5% |
| Conversion Rate | 1-3% / >5% | 0.5-2% / >3% | 0.5-2% / >3% |

**How to calculate:**
- **Engagement Rate** = (Likes + Comments + Shares + LinkClicks) / ImpressionsAdded * 100
- **Click-Through Rate** = LinkClicks / ImpressionsAdded * 100
- **Conversion Rate** = Conversions / LinkClicks * 100

**Network context:**
- LinkedIn consistently outperforms other networks for B2B engagement because the audience is professionally motivated.
- X benchmarks are lower but the platform excels at real-time conversation and industry visibility.
- Facebook B2B performance varies widely by industry; it works best for retargeting and community groups.

---

## Interpretation Patterns

Use these diagnostic patterns when analyzing social performance data:

### Engagement dropped
- Check posting frequency — did volume decrease or increase sharply?
- Review content type mix — has the ratio of promotional vs educational content shifted?
- Look at posting times — were posts published outside peak engagement windows?
- Compare against industry events or holidays that may have suppressed feed activity.

### Clicks up but conversions flat
- The social content is working; the problem is downstream. Check the landing page experience, offer relevance, or form friction.
- Verify that conversion tracking pixels are firing correctly.
- This is not a social issue — do not change the social strategy in response.

### Advocacy outperforming organic
- Employee shares are generating more clicks and conversions than company page posts. This is common in B2B.
- Use this data to build the case for expanding the advocacy program: more advocates, more frequent stories, dedicated advocacy content.

### Impressions high but engagement low
- Content is reaching the audience but not resonating. The distribution is fine; the message needs work.
- Test different hooks, formats (video, carousel, poll), or topics.
- Check if the audience targeting is too broad.

### General analysis principles
- Week-over-week trends matter more than absolute numbers. A single week's data is noise.
- Always compare apples to apples: same content type, same network, same time range.
- Look at a minimum of 4 weeks of data before drawing conclusions.
- Identify outliers (>2 standard deviations from the mean) and investigate root causes before including or excluding them from trend analysis.

---

## Advocacy ROI Calculation

### Core formula
```
Advocacy ROI = (advocacy_conversions * avg_deal_value) / (program_cost + employee_time_cost)
```

### Key comparisons
- Compare `BoardClicks` vs organic `LinkClicks` to measure advocacy traffic uplift.
- Compare `BoardConverts` vs organic `Conversions` to measure advocacy conversion uplift.
- Calculate cost-per-click for advocacy: program_cost / BoardClicks. Compare against paid social CPC.

### Per-advocate efficiency
- Total board engagement (clicks + shares) / number of active advocates = average engagement per advocate.
- Identify top 10% advocates by volume and engagement — these are your advocacy champions.
- Track advocate participation rate: active advocates / total invited advocates. Below 30% signals a content or incentive problem.

---

## Social BI Dashboard Interpretation

When working with Oktopost Social BI dashboard reports:

- Dashboard reports return raw data rows. Your job is to interpret trends across time periods, not just report snapshots.
- Always compare against the prior period automatically when data permits (this week vs last week, this month vs last month).
- Highlight outliers — any metric that deviates more than 2 standard deviations from its rolling average deserves a callout.
- Tie every metric back to a business outcome:
  - `LinkClicks` and `Conversions` connect to pipeline and lead generation.
  - `ImpressionsAdded` and `Reach` connect to brand awareness.
  - `BoardClicks` and `BoardConverts` connect to advocacy program value.
  - `Likes`, `Comments`, and `Shares` connect to audience engagement and content quality.
- When data is sparse (fewer than 10 posts in a period), flag that sample size limits confidence in any conclusions.

---

## Reporting Templates

### Weekly Digest
Structure for a weekly social performance summary:

1. **Top 3 performing posts** — by engagement rate, with network and content type noted.
2. **Engagement trend** — week-over-week change in total engagement, clicks, and impressions.
3. **Advocacy highlight** — top advocacy story, number of active advocates, board click volume.
4. **Action items** — what to double down on, what to stop, what to test next week.

### Campaign Wrap-Up
Structure for end-of-campaign reporting:

1. **Goals vs actuals** — original targets for reach, clicks, and conversions vs delivered numbers.
2. **Top content** — the 3-5 best-performing posts with engagement data and screenshots.
3. **Network comparison** — which network drove the most clicks, engagement, and conversions.
4. **Advocacy contribution** — what percentage of total engagement came from employee advocacy.
5. **Lessons learned** — what worked, what did not, and specific recommendations for the next campaign.

### Monthly Executive Report
Structure for leadership-level monthly reporting:

1. **Reach and awareness growth** — total impressions, reach, and follower growth vs prior month.
2. **Conversion attribution** — total social conversions, conversion rate trend, top converting campaigns.
3. **Advocacy ROI** — advocacy program metrics, cost-per-conversion comparison vs paid and organic.
4. **Content performance** — highest performing content types and topics, format mix analysis.
5. **Recommendations** — 2-3 specific, actionable recommendations for the next month based on data.
