# Pain Query Framework

Use this file to turn an offer into Reddit-native search language.

The framework is domain-neutral. Do not let GTM, sales, or RevOps examples bias the search if the offer is about a different operating problem.

## Core idea

Pain is not a generic topic. Pain is a concrete operational pressure, failure mode, or urgency signal that a buyer would complain about in plain language.

Do not start with:

- broad category labels like `sales automation`
- brand positioning language from the offer page
- jargon that only the seller would use

Start with:

- the buyer's broken workflow
- the bad outcome they are trying to stop
- the urgent event that makes the problem matter now
- the tool or workaround they are frustrated with

If the user provides an ICP, use it to bias search and scoring, not to assume identity.

Good ICP proxies on Reddit:

- stated role words like `founder`, `revops`, `sales ops`, `vp sales`, `agency owner`
- company-stage clues like `series a`, `first sales hire`, `2 reps`, `new vp sales`
- tool-stack mentions like `HubSpot`, `Salesforce`, `Apollo`, `Clay`, `Lemlist`
- workflow clues like `building outbound`, `routing leads`, `fixing reply rates`
- commercial intent like asking for help, comparing tools, or describing a broken buying process

Weak ICP proxies:

- subreddit membership alone
- generic professional language
- broad interest in a topic without owning the problem

## Noise filters

Use these before you trust a hit.

### Hard exclusions

Drop the thread if it is primarily:

- the author's own product or service promotion
- an AMA intended to sell the author's tool
- a hiring post or recruiter-style request
- a cofounder search or partner search
- a sponsorship or monetization request
- a launch or feedback request for the author's own product
- an official vendor or branded-community post
- a duplicate cross-post with the same salesy framing

### Slop penalties

Lower the score when the thread has one or more of these:

- heavy AI buzzwords with little concrete operational detail
- generic frameworks or listicles with no lived failure mode
- improbable claims with no supporting specifics
- vague storytelling that never names the broken workflow
- obvious SEO or content-marketing structure

Concrete detail beats polished language.

## Domain grounding

Before you write search queries, write down the domain nouns that define the operating context.

Examples:

- vendor management
- procurement
- supplier performance
- fulfillment
- 3PL
- IT operations
- support escalation
- renewals
- QBR
- category management
- AML
- KYC
- KYB
- sanctions screening
- transaction monitoring
- underwriting
- loan origination
- credit policy
- manual review
- exceptions

Then force those nouns into the query set so the search does not drift into a neighboring function that happens to share one term.

Examples:

- bad: `qbr metrics`
- better: `3pl qbr metrics`
- better: `vendor qbr prep`
- bad: `renewal leverage`
- better: `vendor renewal leverage procurement`
- bad: `support issues`
- better: `vendor support cases scattered`
- bad: `credit decision engine`
- better: `manual underwriting queue bank`
- better: `loan origination exceptions bank`
- bad: `regtech`
- better: `kyc backlog bank`
- better: `sanctions screening false positives bank`

If the offer is in a regulated-finance domain, avoid consumer borrower language unless the buyer is actually the borrower. Prefer operator workflow terms used by compliance, risk, onboarding, underwriting, and operations teams.

## Query families

Build searches in these buckets.

### 1. Exact pain

Use the literal operational problem.

Examples:

- `founder led sales not scaling`
- `cold outreach low reply rates`
- `too many sales tools not integrated`
- `manual lead research takes forever`

### 2. Symptom or frustration

Use what the buyer feels before they can name the root problem.

Examples:

- `outbound emails getting no replies`
- `pipeline is inconsistent every month`
- `prospecting is taking all day`
- `crm data is a mess`

### 3. Broken workflow

Use the job they are trying to do and where it breaks.

Examples:

- `first sales hire building outbound process`
- `founder still doing prospecting`
- `new vp sales needs pipeline fast`
- `managing outbound with spreadsheets`

### 4. Tool, process, or counterpart complaint

Use a tool name, process, portal, provider type, or counterpart plus frustration language.

Examples:

- `apollo personalization not working`
- `zoominfo too expensive`
- `vendor portal is a mess`
- `3pl communication is a nightmare`

### 5. Trigger event or urgency

Use the business moment that sharpens the pain.

Examples:

- `board wants pipeline numbers`
- `series a outbound setup`
- `new sales leader needs pipeline`
- `hiring sdrs but no process`

## Translation method

1. Read the offer and write 3-6 seller-side pain statements.
2. Rewrite each statement into the way a buyer would complain about it on Reddit.
3. Strip adjectives and claims until the query sounds like something a real person would type.
4. Keep each search phrase short. Most good searches are 3-8 words.
5. Prefer several related searches over one long exact-match search.
6. If a phrase is too generic, anchor it with buyer context such as role, company type, or workflow.

## Translation examples

The examples below are illustrative. Match the offer's domain.

### GTM-style offer

Seller-side statement:

- `Founder-led sales is capping growth`

Reddit-native searches:

- `founder led sales not scaling`
- `founder still doing sales`
- `how to get out of founder led sales`

Seller-side statement:

- `Point tools exist, but there is no ops layer connecting them`

Reddit-native searches:

- `too many sales tools not integrated`
- `sales tools disconnected workflow`
- `revops stack is messy`

Seller-side statement:

- `Cold outreach reply rates are too low`

Reddit-native searches:

- `cold emails getting no replies`
- `outbound reply rates terrible`
- `personalized outreach still not working`

Anchored variants when the raw phrase is noisy:

- `cold email no replies b2b`
- `saas outbound getting no replies`
- `sales outreach no replies founder`

### Vendor-management offer

Seller-side statement:

- `Vendor support evidence is scattered across portals and inboxes`

Reddit-native searches:

- `vendor support cases scattered`
- `support portal vendor nightmare`
- `vendor ticket updates lost in email`

Seller-side statement:

- `Procurement renews without performance leverage`

Reddit-native searches:

- `vendor renewal no leverage`
- `procurement renewal vendor performance`
- `renewing suppliers without scorecard`

Seller-side statement:

- `QBRs are anecdotal because the team lacks measurable vendor evidence`

Reddit-native searches:

- `vendor qbr prep spreadsheet`
- `supplier qbr metrics`
- `qbr with vendors no data`

Seller-side statement:

- `3PL and fulfillment partners are managed through fragmented reporting`

Reddit-native searches:

- `3pl scorecard spreadsheet`
- `fulfillment vendor performance tracking`
- `3pl qbr metrics`

### Regulated-finance offer

Seller-side statement:

- `Sanctions and KYC screening generate too many false positives`

Reddit-native searches:

- `aml false positives backlog`
- `sanctions screening false positives`
- `kyc alerts manual review`

Seller-side statement:

- `Analysts clear obvious cases by moving data across disconnected systems`

Reddit-native searches:

- `kyc data entry with extra steps`
- `compliance backlog manual review`
- `screening hits across multiple systems`

Seller-side statement:

- `Credit approvals and underwriting rules are slow to change`

Reddit-native searches:

- `manual underwriting queue`
- `loan approval turnaround slow`
- `credit policy changes take months`

Seller-side statement:

- `Borderline cases fall out to exceptions and manual review`

Reddit-native searches:

- `loan origination exceptions`
- `kyc fails before manual review`
- `account frozen compliance review`

## What to avoid

- Do not search only the product category.
- Do not rely on one exact phrase.
- Do not assume the user knows the root cause.
- Do not overfit to seller vocabulary if buyer vocabulary is plainer.
- Do not keep generic phrases unanchored when results drift into consumer, entertainment, or unrelated life problems.
- Do not pretend a Reddit username or one post proves the person matches the ICP.
- Do not let promotional or AI-slop posts survive just because they mention the right tools or buzzwords.
- Do not reuse GTM-flavored example wording when the offer lives in a different domain.
- Do not lead with abstract platform terms like `decision engine`, `AI underwriting`, or `regtech` when the goal is to find pain. Those phrases attract vendor content faster than operator complaints.
