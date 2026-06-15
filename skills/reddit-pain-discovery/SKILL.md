---
name: reddit-pain-discovery
description: Turn an offer URL or offer summary into pain-first Reddit search queries and run the Apify Reddit scraper to find threads where prospects describe the problem in their own words. Use when the user asks to find pain, complaints, buying signals, or conversation opportunities on Reddit for a product, offer, or ICP.
---

# Reddit Pain Discovery

Convert an offer into ranked Reddit conversations that expose real buyer pain and reply opportunities.

## Use This Skill To Produce

- A compact summary of the offer, ICP, and likely buyer language
- 8-20 pain-first Reddit search queries grouped by query family
- One or more bounded Apify runs using `harshmaur/reddit-scraper`
- Ranked threads with evidence, fit, urgency, and a reply angle

## Inputs

- Prefer an offer URL. If absent, use a short offer description.
- Optional: ICP, target subreddits, excluded subreddits, time window, spend cap, or whether to crawl comments.

## Rules

- Before building queries, inspect skill-local memory under `memory/domains/` and `memory/urls/`.
- Review `memory/lessons.md` first for global rules learned across prior runs.
- Treat `memory/domains/` as reusable domain tuning and `memory/urls/` as offer- or page-specific tuning.
- Reuse stable tuning from memory unless fresh live results contradict it.
- Search for concrete pains, symptoms, trigger events, and tool complaints, not just category keywords.
- Start broad, then narrow using the language that actually surfaces useful threads.
- If a symptom phrase is too generic, add buyer-context anchors such as role, company type, or workflow (`b2b`, `saas`, `sales`, `revops`, `founder`) or narrow with `withinCommunity`.
- Keep the first pass cheap. Do not crawl deep comments until posts are promising.
- Treat Reddit as signal discovery. It is evidence of language and urgency, not proof of TAM.
- Always report the `search window used` separately from the `actual age cutoff applied`.
- Never describe a run as `last 48 hours`, `fresh`, or `live opportunities` unless posts were explicitly filtered to a true rolling 48-hour cutoff from `createdAt`.
- If an ICP is provided, use it as a scoring prior, not a hard gate.
- Separate `thread fit` from `person fit`. A thread can be highly relevant even when the author's exact persona is unknown.
- When persona evidence is weak, mark confidence as `unknown` instead of pretending low-confidence inference is certainty.
- After ranking, classify each surviving thread into an engagement mode: `ignore`, `monitor`, `public reply`, or `dm only`.
- Default to `public reply` over `DM` when a useful public contribution is possible.
- Use `dm only` sparingly: only when the thread explicitly asks for private follow-up, requests vendor recommendations off-thread, or subreddit norms make public vendor participation inappropriate.
- Do not use `DM me` or soft-gated CTA language in public replies.
- When asked for a reply, write a thread-specific reply that references concrete facts from the post and gives real help. Do not generate generic “example replies.”
- Before drafting a reply, classify the thread using `references/reply-modes.md`.
- Replies should sound like a practitioner, not a marketer: casual, concrete, and useful. Avoid pitches unless the user explicitly wants a commercialization pass.
- Prefer 2-4 short paragraphs over one dense block.
- Avoid em dashes, semicolons, and colon-heavy phrasing in drafted replies because they make the comment read overly polished or AI-shaped.
- Prefer plainspoken wording over compressed, high-density phrasing.
- Match the thread's emotional frame. A vent thread needs pattern recognition and restraint, not a management framework.
- If a thread is mostly venting about an industry-wide pattern, do not force `QBR`, `scorecard`, `RCA`, or procurement-process language unless the author is already speaking that way.
- If the author accuses the reply of being AI, fake, or shilly, do not defend the toolchain, do not explain how the comment was written, and do not keep arguing. Disengage.
- Hard-drop obvious self-promo, owned-channel marketing, hiring posts, cofounder ads, newsletter sponsor asks, official vendor content, and pure product-launch threads unless the user explicitly wants supply-side research.
- Apply a second penalty layer for low-substance AI slop so buzzword-heavy threads do not outrank real operator pain.
- Penalize hobbyist, student, meme, and off-topic threads unless the user explicitly wants them.
- In regulated or highly specialized domains, avoid abstract category phrases such as `decision engine`, `regtech`, or `AI underwriting` until real operator language is proven. Prefer queue, backlog, false positive, exception, turnaround, and policy-change wording first.
- After each substantive run, update or create the relevant memory note with winning queries, losing queries, good communities, bad communities, exclusion cues, and domain-specific language learned from the run.
- Verify the live Actor schema before running the scraper.
- Prefer the Apify tool surface when it is available in the current run.
- Otherwise use an authenticated `apify` CLI session.
- Use the result template in `assets/finding-template.md`.

## Workflow

1. Inspect memory.
   - Read `memory/lessons.md` first.
   - If a URL is available, run `python3 scripts/resolve_memory.py --url "<offer_url>" --scaffold`.
   - Use the script output to find the matching domain note and URL note.
   - Treat these notes as priors, not truth. Live results can override them.

2. Read the offer.
   - Open the URL or inspect the provided summary.
   - Extract: ICP, promised outcome, broken alternatives, costly symptoms, urgency triggers, and named tools or competitors.

3. Translate the offer into pain primitives.
   - Build 3-6 concrete pain statements.
   - Build the phrases prospects would type when they feel those pains.
   - Build adjacent symptom phrases, trigger-event phrases, and tool-complaint phrases.
   - If an ICP is given, extract the strongest observable proxies: role words, company stage, team shape, tools, workflow, and urgency triggers.
   - Use `references/pain-query-framework.md`.

4. Build query families.
   - Create 2-4 searches for each family:
   - Exact pain
   - Symptom or frustration
   - Broken workflow
   - Tool or competitor complaint
   - Trigger event or urgency
   - Add at least one anchored variant when the raw phrase can collide with consumer or general-interest topics.
   - Keep searches short and human. Prefer phrases users would post, not internal positioning copy.

5. Choose the search shape.
   - Discovery mode defaults:
   - `searchPosts=true`
   - `searchComments=false`
   - `searchCommunities=false`
   - `searchSort="relevance"`
   - `searchTime="month"` or `"week"`
   - `maxPostsCount=10`
   - no `withinCommunity`
   - Engagement mode defaults:
   - `searchPosts=true`
   - `searchComments=false`
   - `searchCommunities=false`
   - `searchSort="new"` or `"relevance"`
   - `searchTime="day"` or `"week"`
   - after retrieval, filter to `createdAt >= now - 48h` when the user wants a real last-48-hours queue
   - Default pass 2:
   - use winning subreddits from pass 1
   - optionally set `withinCommunity`
   - optionally enable `crawlCommentsPerPost=true`
   - cap `maxCommentsPerPost` tightly

6. Run the Actor.
   - Fetch schema and confirm any field changes against `references/apify-reddit-scraper.md`.
   - If the Apify tool surface is available:
   - use the equivalent `fetch actor details`, `call actor`, `get actor run`, and `get dataset items` flow with actor `harshmaur/reddit-scraper`
   - keep the first pass bounded with a small spend cap when the tool surface supports it
   - If the Apify tool surface is not available but the `apify` CLI is authenticated:
   - run `apify actors info harshmaur/reddit-scraper --input` to confirm the input schema
   - save the actor input JSON to a local file
   - run `apify call harshmaur/reddit-scraper --input-file <input.json> --silent --json`
   - inspect the returned run metadata and fetch items with `apify datasets get-items <datasetId>`
   - If neither path exists, say that live Reddit scraping is blocked and stop instead of pretending the run happened.

7. Rank and filter.
   - Start with hard exclusions:
   - explicit self-promo or founder AMA for the author's own product
   - official brand or vendor-owned subreddit content
   - hiring posts, recruiter posts, cofounder-seeking posts, service offers
   - launch posts, sponsor-hunting posts, and direct product feedback asks
   - identical or near-identical cross-post spam
   - Then score each surviving thread on:
   - Score each thread on:
   - pain specificity
   - thread-level ICP fit
   - author-level ICP likelihood
   - buyer fit
   - urgency
   - engagement
   - reply opportunity
   - Use explicit evidence only: subreddit context, stated role, company clues, tool mentions, hiring or stage language, and commercial intent.
   - If the author cannot be classified, keep the thread if the problem and context are strong.
   - Apply slop penalties for:
   - generic AI buzzword stuffing without concrete operating detail
   - listicle or thought-leadership formatting with no first-hand failure mode
   - impossible or ungrounded claims with no evidence
   - vague build-in-public narration that does not expose a real pain or buying signal
   - content that reads like SEO bait more than a lived operating problem
   - Penalize generic discussion, memes, homework, or obvious low-fit audiences.
   - Then assign an engagement mode:
   - `ignore`: low-fit, promo, slop, hobbyist, or no useful contribution available
   - `monitor`: relevant language or market context, but weak buyer fit or no credible reply angle yet
   - `public reply`: strong problem fit and a concrete public contribution can help the author or thread
   - `dm only`: private follow-up is clearly invited or norm-safe, and a public reply would be awkward or counterproductive

8. Present the findings.
   - Use the structure in `assets/finding-template.md`.
   - State both the Actor `searchTime` and any stricter post-run age cutoff.
   - Show the search family that found each thread.
   - Include the matched pain, evidence snippet, why it matters, the engagement mode, and a suggested reply or research angle.
   - If the user asks for a reply, provide a concrete draft for the highest-priority threads. The draft must be specific to the thread, not a generic template.
   - Note the `reply mode` used for each drafted reply when it affects tone or structure.

9. Update memory.
   - Update `memory/lessons.md` when a lesson should apply across domains and future offers.
   - Update the domain note when the learning is reusable across the company or category.
   - Update the URL note when the learning depends on a specific page, wedge, ICP, or offer framing.
   - Record what worked, what drifted, and which communities were productive.

10. Iterate only after reviewing pass 1.
   - Expand the best-performing wording into follow-up searches.
   - Narrow to subreddits only after the broad language is proven.

## Deliverable Format

- `Offer summary`: ICP, outcome, pains, triggers
- `Query set`: grouped by search family
- `Run config`: the Actor input actually used
- `Freshness`: search window used, whether a stricter age cutoff was applied, and the exact cutoff rule when relevant
- `Findings`: ranked list from `assets/finding-template.md`, including `thread fit`, `person fit`, `persona confidence`, and any exclusion or slop flags
- `Engagement`: for each kept thread, include `engagement mode` and, when requested, a concrete draft reply
- `Memory updates`: note files created or updated, and the main tuning captured
- `Next moves`: follow-up queries, subreddits, or comment-deepening steps
