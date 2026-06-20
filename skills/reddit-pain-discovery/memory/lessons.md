# Lessons Learned

## Format

Each lesson follows this structure:

```markdown
### YYYY-MM-DD | [Context]
**What happened:** [What drifted, what was corrected, or what was learned]
**Rule:** [Concrete rule to apply on future runs]
```

## Entries

### 2026-06-15 | ICP scoring and evidence quality
**What happened:** Early versions of the skill treated weak persona clues too confidently.
**Rule:** Separate `thread fit` from `person fit`, and mark persona confidence as `unknown` when Reddit evidence is weak.

### 2026-06-15 | Promo and AI-slop contamination
**What happened:** Posts mentioning the right tools or buzzwords could outrank real operator pain even when they were self-promotional or low-substance.
**Rule:** Hard-drop self-promo first, then apply a second slop-penalty layer so lived workflow pain outranks polished marketing content.

### 2026-06-15 | Domain drift from generic terms
**What happened:** Generic phrases such as `QBR`, `renewal`, or `support` drifted into unrelated functions unless domain nouns were forced into the query set.
**Rule:** When a domain has strong operating nouns, anchor every query family with those nouns before broadening.

### 2026-06-15 | Regulated-finance query shaping
**What happened:** Terms like `decision engine`, `regtech`, and `AI underwriting` pulled vendor content and consumer noise faster than operator complaints.
**Rule:** In regulated-finance domains, start with operator language such as backlog, false positives, manual review, exceptions, turnaround time, and policy-change latency.

### 2026-06-15 | Domain vs. URL memory
**What happened:** Some tuning was reusable at the company level, while some depended on a specific offer page like `/exo`.
**Rule:** Store reusable drift patterns in domain notes and wedge-specific tuning in URL notes.

### 2026-06-15 | Community discovery for fragile domains
**What happened:** In specialized domains like credit decisioning, broad Reddit search looked non-viable until a separate community-discovery pass identified narrow operator subreddits.
**Rule:** When broad search quality is poor but the domain may still exist on Reddit, discover communities first and then judge viability from bounded community passes.

### 2026-06-15 | Raw volume vs usable threads
**What happened:** Fresh reruns for GTM and procurement-adjacent offers surfaced large raw result counts, but much of the volume was seller chatter, self-promo, or keyword drift rather than buyer pain.
**Rule:** Report raw post volume separately from the smaller kept set, and treat broad-count inflation as a warning that precision needs stronger anchors or community narrowing.

### 2026-06-15 | Public reply before DM
**What happened:** The strongest repository guidance and best engagement evidence favored useful public comments over gated or private follow-up.
**Rule:** Default to `public reply` when a concrete public contribution is possible. Reserve `dm only` for explicit invitation or norm-sensitive cases.

### 2026-06-15 | Search window vs actual freshness
**What happened:** Discovery runs used broad actor time windows like `month`, but that can be mistaken for a true last-48-hours feed if the report is sloppy.
**Rule:** Always report actor `searchTime` separately from any post-run `createdAt` cutoff. Only call a queue `last 48 hours` when a true rolling 48-hour filter was applied.

### 2026-06-15 | Vent threads are not operator-advice threads
**What happened:** A reply that used process language like `scorecard`, `QBR`, and `RCA` landed badly in a thread that was mainly venting about an industry-wide support decline.
**Rule:** Classify reply mode before drafting. Vent threads need pattern recognition and restraint, not a management framework. If the author calls the reply AI or shilly, disengage instead of defending the toolchain.

### 2026-06-18 | Goodput beats visibility
**What happened:** It became too easy to treat broad relevance or audience visibility as success even when the surfaced threads were weak engagement opportunities.
**Rule:** Optimize Reddit discovery for goodput. Count only threads with substantive external discussion and a credible public-engagement angle as success. Visibility-only hits belong in tuning notes, not in the win column.

## Active Rules

1. Read `lessons.md` before building queries.
2. Reuse domain and URL notes as priors, not truth.
3. Separate thread relevance from persona certainty.
4. Drop self-promo before scoring.
5. Penalize AI slop even when it uses the right keywords.
6. Force domain nouns into generic query families.
7. Use operator workflow language before platform-category language in specialized domains.
8. For fragile domains, run community discovery before declaring Reddit non-viable.
9. Separate raw surfaced-post counts from the smaller kept set.
10. Default to public reply before DM.
11. Report search window and actual age cutoff separately.
12. Optimize for goodput, not visibility-only relevance.
