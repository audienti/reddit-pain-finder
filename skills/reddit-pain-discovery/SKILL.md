---
name: reddit-pain-discovery
description: Turn an offer URL or offer summary into Reddit signal queries and run the Apify Reddit scraper to find threads worth engaging now for buyer signal or audience visibility. Use when the user asks to find signals, buyer language, pain, or conversation opportunities on Reddit for a product, offer, or ICP.
---

# Reddit Signal Discovery

Convert an offer into ranked Reddit conversations that are worth engaging now
for buyer signal or audience visibility.

## Use This Skill To Produce

- A compact summary of the offer, ICP, and likely buyer language
- 8-20 pain-first Reddit search queries grouped by query family
- One or more bounded Apify runs using `harshmaur/reddit-scraper`
- Ranked threads with evidence, fit, urgency, and a reply angle
- A track split across base direct-demand retrieval and additive
  visibility-leverage retrieval
- An outcome split across `direct_buyer`, `visibility_leverage`, or `discard`
- A surface split across `buyer_authored`, `competitor_audience`,
  `creator_audience`, `community_audience`, or `partner_audience`
- A goodput run ledger that records `query -> seeds -> scraped threads -> external substantive discussion -> goodput opportunities -> posted engagement`

## Inputs

- Prefer an offer URL. If absent, use a short offer description.
- Optional: ICP, target subreddits, excluded subreddits, time window, spend cap, or whether to crawl comments.

## Brand-Building Frame

- Treat this skill as a recurring brand-building and market-learning system, not a one-shot buyer export.
- Dedupe exact posts and near-duplicate threads, not authors forever.
- Repeated appearances from the same author, subreddit, or problem cluster can be positive if the new thread adds fresh context and is not just repeated self-promo.
- Classify kept hits into repeat status:
- `net_new`
- `known_good_repeat`
- `new_voice_in_known_cluster`
- `already_engaged_surface`
- Penalize repetition only when it is recycled self-promo, audience farming, or low-substance posting.

## Rules

- Before building queries, inspect skill-local memory under `memory/domains/`, `memory/urls/`, and `memory/icps/` when an ICP is present.
- Inspect the resolved `memory/seed_packs/` note before inventing new queries so proven communities, authors, and thread shapes get reused.
- Inspect the resolved `memory/run_ledgers/` note before spending more so the run is measured against prior goodput, not just recall.
- Inspect the resolved `memory/comments/` note before drafting a reply so the run stays aware of prior public engagement.
- Review `memory/lessons.md` first for global rules learned across prior runs.
- Treat `memory/domains/` as reusable domain tuning and `memory/urls/` as offer- or page-specific tuning.
- Treat `memory/icps/` as the primary prior when the exact offer plus buyer lens has been tuned before.
- Separate `strategy` from `surface_family`.
- Strategy answers `why this is worth engaging commercially`.
- Surface family answers `whose authored surface or audience produced the
  signal`.
- Use `buyer_authored` for direct operator threads and the other surface
  families for competitor, creator, community, or partner audiences.
- Never let competitor, influencer, partner, or adjacent-offer surface
  tracking replace direct pain, topic, symptom, or recommendation retrieval.
- A full run should usually keep one base direct-demand track such as
  `direct_buyer + buyer_authored`, then add one or more visibility-leverage
  tracks such as `visibility_leverage + creator_audience` or
  `visibility_leverage + competitor_audience`.
- Reuse stable tuning from memory unless fresh live results contradict it.
- Optimize for `goodput`, not raw relevance or visibility.
- A hit only counts as success when it exposes substantive external discussion and a credible public-engagement angle after promo, slop, and low-fit suppression.
- The returned queue is `raw surfaces -> engage_now -> discard`.
- There is no watchlist, deepen-later, or maybe bucket in the published
  contract. If it is not worth engaging now, discard it.
- Search for concrete pains, symptoms, trigger events, and tool complaints, not just category keywords.
- Start broad, then narrow using the language that actually surfaces useful threads.
- If a symptom phrase is too generic, add buyer-context anchors such as role, company type, or workflow (`b2b`, `saas`, `sales`, `revops`, `founder`) or narrow with `withinCommunity`.
- Keep the first pass cheap. Do not crawl deep comments until posts are promising.
- Treat Reddit as signal discovery. It is evidence of language and urgency, not proof of TAM.
- Broad all-Reddit search is exploratory only. Default to bounded communities,
  named audience surfaces, or seeded subreddits when you need real goodput.
- Always report the `search window used` separately from the `actual age cutoff applied`.
- Never describe a run as `last 48 hours`, `fresh`, or `live opportunities` unless posts were explicitly filtered to a true rolling 48-hour cutoff from `createdAt`.
- If an ICP is provided, use it as a scoring prior, not a hard gate.
- Separate `thread fit` from `person fit`. A thread can be highly relevant even when the author's exact persona is unknown.
- When the strategy is `visibility_leverage`, prefer
  seeded named competitors, creators, adjacent communities, or partners before
  inventing wider open query families.
- When persona evidence is weak, mark confidence as `unknown` instead of pretending low-confidence inference is certainty.
- Report whether each kept hit is `net new`, `repeat from known-good cluster`, or `already engaged in this cluster`.
- After ranking, classify each surviving thread into an action type: `engage_now` or `discard`.
- Default to `public reply` over `DM` when a useful public contribution is possible.
- Use `dm only` sparingly: only when the thread explicitly asks for private follow-up, requests vendor recommendations off-thread, or subreddit norms make public vendor participation inappropriate.
- Do not use `DM me` or soft-gated CTA language in public replies.
- When asked for a reply, write a thread-specific reply that references concrete facts from the post and gives real help. Do not generate generic “example replies.”
- Do not reuse the same comment angle against the same author, thread, or cluster when the comment log shows it was already used recently.
- Before drafting a reply, classify the thread using `references/reply-modes.md`.
- Replies should sound like a practitioner, not a marketer: casual, concrete, and useful. Avoid pitches unless the user explicitly wants a commercialization pass.
- Prefer 2-4 short paragraphs over one dense block.
- Avoid em dashes, semicolons, and colon-heavy phrasing in drafted replies because they make the comment read overly polished or AI-shaped.
- Prefer plainspoken wording over compressed, high-density phrasing.
- Match the thread's emotional frame. A vent thread needs pattern recognition and restraint, not a management framework.
- If a thread is mostly venting about an industry-wide pattern, do not force `QBR`, `scorecard`, `RCA`, or procurement-process language unless the author is already speaking that way.
- If the author accuses the reply of being AI, fake, or shilly, do not defend the toolchain, do not explain how the comment was written, and do not keep arguing. Disengage.
- Hard-drop obvious self-promo, owned-channel marketing, hiring posts, cofounder ads, newsletter sponsor asks, official vendor content, and pure product-launch threads unless the user explicitly wants supply-side research.
- Down-rank authors or communities that repeatedly surface but only as recycled self-promo, copied advice, or low-substance noise.
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
   - Resolve the base direct-demand track first.
   - Then resolve additive surface tracks one by one so buyer-authored pain
     priors and audience-surface priors stay separate.
   - If a URL is available, run `python3 scripts/resolve_memory.py --url "<offer_url>" --icp "<icp>" --strategy "<strategy>" --surface-family "<surface_family>" --scaffold` when an ICP, strategy, or surface family is present, otherwise omit the optional flags.
   - Use the script output to find the matching domain note and URL note.
   - If an ICP note exists, treat it as the primary prior for that exact run shape.
   - Use the same script output to find the seed-pack, run-ledger, and comment notes for the exact strategy and surface-family combination being tuned.
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
   - Build the retrieval stack in this order:
   - base direct-demand track: pain, topic, symptom, trigger-event,
     recommendation, and workflow-debug retrieval from likely buyer-authored
     surfaces
   - additive visibility-leverage tracks: competitors, influencers, consultants,
     communities, partners, or adjacent offers speaking to the same audience
   - Do not drop the base direct-demand track just because a surface track
     exists.
   - Build a surface map before expanding open search:
   - `buyer_authored`: direct operators or likely buyers describing their own
     problem
   - `competitor_audience`: competitor or adjacent vendor threads with
     overlapping buyer audiences
   - `creator_audience`: consultants, coaches, educators, or influencers
   - `community_audience`: niche communities where the ICP gathers
   - `partner_audience`: implementation, tooling, or service partners
   - If the motion is `visibility_leverage`, start from
     named surface seeds first and only then widen into open query families.
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
   - save dataset items to a local JSON file
   - run `python3 scripts/normalize_apify_search_results.py --input <dataset.json>`
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
   - Then assign an action type:
   - `engage_now`: the thread is strong enough to reply to now
   - `discard`: low-fit, promo, slop, hobbyist, or no credible reply path
   - Also assign repeat status:
   - `net_new`
   - `known_good_repeat`
   - `new_voice_in_known_cluster`
   - `already_engaged_surface`
   - Track the surface family for each kept thread so direct pain discovery is
     not blended with competitor, creator, or community-audience motions.

8. Present the findings.
   - Use the structure in `assets/finding-template.md`.
   - State both the Actor `searchTime` and any stricter post-run age cutoff.
   - Report the shared goodput funnel:
   - `query count`
   - `seed count`
   - `scraped threads`
   - `external substantive discussion`
   - `goodput opportunities`
   - `posted engagement`
   - Report the track split clearly so direct pain/topic opportunities stay
     separate from competitor, influencer, and audience-surface opportunities.
   - Report both the outcome split and the surface split clearly.
   - Show the search family that found each thread.
   - Include the matched pain, evidence snippet, why it matters, the action type, the repeat status, and a suggested reply or research angle.
   - If the user asks for a reply, provide a concrete draft for the highest-priority threads. The draft must be specific to the thread, not a generic template.
   - Note the `reply mode` used for each drafted reply when it affects tone or structure.

9. Update memory.
   - Update `memory/lessons.md` when a lesson should apply across domains and future offers.
   - Update the domain note when the learning is reusable across the company or category.
   - Update the URL note when the learning depends on a specific page, wedge, ICP, or offer framing.
   - Update the ICP note when the learning depends on a specific buyer lens.
   - Update the seed-pack note when a query, subreddit, author cluster, or
     surface family proves durable enough to reuse.
   - Update the run-ledger note after every live run using the normalizer output so all future comparisons use the same funnel.
   - Update the comment note when a reply is drafted, posted, edited, ignored, or gets a meaningful response.
   - Record what worked, what drifted, which communities were productive, which authors or threads deserve active follow-up after posting, and which repeats were useful versus repetitive noise.

10. Iterate only after reviewing pass 1.
   - Expand the best-performing wording into follow-up searches.
   - Narrow to subreddits only after the broad language is proven.
   - Re-seed later runs from known-good subreddits, authors, and thread clusters before inventing a fully new query set.

## Deliverable Format

- `Offer summary`: ICP, outcome, pains, triggers
- `Query set`: grouped by search family
- `Run config`: the Actor input actually used
- `Freshness`: search window used, whether a stricter age cutoff was applied, and the exact cutoff rule when relevant
- `Goodput`: `query count`, `seed count`, `scraped threads`, `external substantive discussion`, `goodput opportunities`, `posted engagement`, and the primary failure mode
- `Track split`: counts for `direct_demand` and `visibility_leverage`
- `Outcome split`: counts for `direct_buyer`, `visibility_leverage`, and `discard`
- `Surface split`: counts for `buyer_authored`, `competitor_audience`,
  `creator_audience`, `community_audience`, and `partner_audience`
- `Findings`: ranked list from `assets/finding-template.md`, including `thread fit`, `person fit`, `persona confidence`, `repeat status`, and any exclusion or slop flags
- `Action`: for each kept thread, include `action type` and, when requested, a concrete draft reply
- `Comment tracking`: the resolved comment note path and any entries that should be added or updated
- `Run ledger`: the resolved run-ledger path and the row that should be appended
- `Memory updates`: note files created or updated, and the main tuning captured
- `Next moves`: follow-up queries, subreddit or author surface expansions, or live reply follow-up after we have already engaged
