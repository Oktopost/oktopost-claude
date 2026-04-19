# Oktopost Workflows and Campaign Lifecycle

Reference for B2B social media campaign workflows, approval patterns, and operational best practices in Oktopost.

---

## Campaign Lifecycle

Every B2B social initiative follows this standard flow:

1. **Plan** — Define the campaign goal (awareness, lead gen, event registration), target audience, networks, and timeline.
2. **Create Campaign** — Set up the campaign in Oktopost with a descriptive name, date range, and associated tags. The campaign is the top-level container for all attribution.
3. **Draft Messages** — Write message variations tailored to each network. A single campaign typically has 3-8 messages covering different angles.
4. **Create Posts** — Assign messages to specific social profiles, networks, and time slots. Each message can generate multiple posts across profiles.
5. **Approval** — Route posts through the appropriate approval workflow before they go live. Required for compliance-sensitive industries.
6. **Schedule** — Confirm publish dates and times. Stagger posts to avoid audience fatigue.
7. **Publish** — Oktopost publishes posts at their scheduled times via connected social profiles.
8. **Analyze** — Review engagement, clicks, conversions, and advocacy metrics against campaign goals.
9. **Iterate** — Double down on high-performing content, retire underperformers, adjust timing and frequency.

---

## Multi-Step Workflow Templates

### Product or Feature Launch

1. Create a campaign named with the feature and quarter (e.g., `AI-Assist-Launch-Q3-2026`).
2. Draft 5-7 messages: teaser, announcement, feature deep-dive, customer quote, demo CTA, recap.
3. Create posts for LinkedIn (company page + executive profiles), X, and Facebook.
4. Set up an advocacy board story so employees can amplify the announcement.
5. Confirm the campaign name matches the customer's Oktopost campaign taxonomy -- Oktopost will auto-append the campaign UTM at publish time based on this name.
6. Schedule teaser 3 days before launch, announcement on launch day, follow-up posts over the next 2 weeks.
7. Route all posts through approval workflow before scheduling.
8. Monitor engagement daily for the first week; boost top performers with additional advocacy pushes.

### Event or Webinar Promotion

1. Create a campaign tied to the event (e.g., `Webinar-ABM-Masterclass-Apr2026`).
2. Pre-event series (2-3 weeks out): registration CTA, speaker spotlight, agenda highlights. At least 4-5 posts.
3. Day-of posts: "Starting now" reminder, live quote or insight, mid-session engagement prompt.
4. Post-event: thank you post, on-demand recording link, key takeaway thread, attendee testimonial.
5. Use advocacy board to have sales reps share registration links with their networks.
6. Track registrations via Oktopost's auto-appended UTMs (in the okt.to short links); compare advocacy vs organic channel performance in the Oktopost dashboard.

### Thought Leadership Series

1. Create a recurring campaign (e.g., `Thought-Leadership-LinkedIn-Q2-2026`).
2. Establish a consistent posting cadence: 2-3 LinkedIn posts per week from executive profiles.
3. Draft messages with a consistent voice and thematic thread (e.g., "5 things I learned about B2B attribution").
4. Use thread strategy: post a hook, follow up with 2-3 comments adding depth within the first hour.
5. Rotate between formats: text-only insights, carousel documents, short video clips, poll questions.
6. Review engagement weekly; identify which topics and formats resonate most.

### Employee Advocacy Push

1. Create or select an advocacy board in Oktopost.
2. Write board stories with pre-drafted messages employees can share with one click.
3. Provide 2-3 message variations per story so shares look authentic, not templated.
4. Send advocate invites to target groups (sales team, customer success, executives).
5. Enable gamification: set up leaderboards and recognition for top sharers.
6. Track `BoardClicks` and `BoardConverts` to measure advocacy ROI vs organic posting.

### Customer Story or Case Study

1. Create a campaign for the customer story (e.g., `CaseStudy-Acme-Corp-2026`).
2. Get quote approval from the customer before drafting social posts.
3. Adapt content per network: LinkedIn gets the detailed narrative, X gets the punchy stat, Facebook gets the visual.
4. Tag the customer company and relevant individuals where appropriate and permitted.
5. Schedule posts over 1-2 weeks; lead with the headline stat, follow with the full story link.
6. Add the case study to an advocacy board for employee amplification.

---

## Approval Flow Patterns

### Single-Step Approval
- One designated manager reviews and approves all posts before scheduling.
- Best for small teams with low post volume.

### Multi-Step Approval
- Draft creator submits to direct manager, then routed to compliance or legal for final sign-off.
- Required in regulated industries (financial services, healthcare, legal).
- Each step has its own approver and SLA.

### Auto-Approve
- Specific campaigns or trusted users bypass the approval queue.
- Configure per campaign or per user role in Oktopost settings.
- Use for low-risk content like recurring advocacy board stories.

### When to Use `send_to_workflow` vs Direct `create_post`
- Use `send_to_workflow` when the organization requires approval before publishing. This places the post in the approval queue.
- Use `create_post` directly only when the user has publish permissions and no approval workflow is enforced for that campaign.
- When in doubt, default to `send_to_workflow` — it is always safer.

### Stale Workflow Items
- Posts sitting in the approval queue for more than 48 hours risk missing their scheduled window.
- Identify stale items by checking workflow status and comparing against intended publish dates.
- Escalate to the assigned approver or suggest the requester ping them directly.

---

## UTMs — Let Oktopost Handle Them

**The skill does NOT add UTMs to URLs. Oktopost does it automatically.**

When a post publishes, Oktopost shortens the destination URL to `okt.to/xxx` and appends UTM parameters tying the click back to the specific campaign, post, network, and (for advocacy) advocate. Those UTMs are configured once inside the Oktopost product at the account or campaign level -- customers control them there, not in the skill.

**Implications for content generation:**

- Draft content with bare URLs. Do NOT add `?utm_source=...` or any tracking params to links you generate.
- Never ask the user "what UTMs should I use?" -- the answer is "Oktopost's, which are already set up."
- In analytics, when explaining how a post is tracked, say "Oktopost's auto-appended UTMs" -- do not claim the skill added them.

**The only exception: user-supplied hard-coded tracking.**

If the user gives you a destination URL that already contains tracking (e.g., a Marketo landing page with baked-in `?mkt_tok=...` or co-marketing params like `?partner=acme`), pass it through verbatim. Do not strip or "normalize" those params. Oktopost will still wrap the URL in okt.to and add its own UTMs on top -- both systems' attribution will work.

**What you WILL see in reporting:**

The URL that appears in reporting is the okt.to short URL plus Oktopost's UTMs. If a customer asks "why don't I see `utm_source=linkedin`?", the answer is that Oktopost's UTM scheme uses its own field names -- check their Oktopost > Settings > Tracking page to see the exact convention for their account.

---

## Common Mistakes

1. **Publishing without campaign association** — Posts created outside a campaign break attribution. Every post must belong to a campaign for proper tracking and reporting.

2. **Same content across all networks** — LinkedIn, X, and Facebook have different audiences and formats. Adapt tone, length, hashtags, and media for each network.

3. **Skipping approval when compliance requires it** — Even urgent posts must go through workflow in regulated industries. Build buffer time into schedules to accommodate review cycles.

4. **Scheduling all posts at the same time** — Multiple posts from the same brand at the same hour cannibalize each other's reach. Space posts at least 2-4 hours apart; ideally spread across different days.

5. **Ignoring advocacy as a distribution channel** — Employee networks collectively have 10x the reach of company pages. Every major campaign should include an advocacy board story alongside organic posts.

6. **Not tracking results back to campaign goals** — Publishing without reviewing performance means missing optimization opportunities. Check campaign analytics at least weekly during active campaigns.
