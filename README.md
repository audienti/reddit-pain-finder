# Reddit Signal Finder

Reddit Signal Finder is a Codex and Claude Code plugin for turning an offer
into real Reddit threads worth engaging now for buyer signal or audience
visibility.

It is built for signal discovery, language capture, and reply drafting. Instead
of guessing how buyers talk, it helps you find the threads where they are
already saying it.

## What the plugin provides

- A `reddit-pain-discovery` skill under `skills/reddit-pain-discovery/`
- Query-building guidance under `references/`
- A reply-style rubric tuned for Reddit-native engagement
- Skill-local memory for domain, URL, ICP, seed-pack, run-ledger, and comment notes
- A helper script to resolve and scaffold memory note paths
- A helper script to normalize Reddit datasets into the shared goodput funnel
- Codex marketplace metadata at `.codex-plugin/plugin.json`
- Claude Code marketplace metadata at `.claude-plugin/plugin.json`

## Best for

- finding live buyer language before writing outbound
- pressure-testing whether a wedge has live Reddit signal
- surfacing real threads worth public engagement
- drafting useful public replies instead of generic soft pitches
- separating raw result volume from the smaller set of threads that are
  actually worth engaging now

## What it does

The plugin adds a research skill that:

- reads an offer URL or short offer summary
- translates the offer into Reddit signal queries
- runs bounded discovery against `harshmaur/reddit-scraper`
- filters self-promo, weak-fit noise, and AI slop
- measures every run as `query -> seeds -> scraped threads -> external substantive discussion -> goodput opportunities -> posted engagement`
- keeps only the `engage_now` set and discards everything else
- ranks the best threads by fit, urgency, and reply opportunity
- drafts thread-specific replies when asked

## Runtime requirements

This plugin ships a skill. It does not bundle its own MCP server or app
connector.

It works inside Codex by using the tools already available in the current run.

### Required

- Codex plugin support with skill loading enabled
- access to native web research in the current run
- `python3` for the bundled memory resolver script

### Recommended

- an Apify tool surface in the current run
- or an authenticated local `apify` CLI session

### What happens without them

- without Apify tooling or an authenticated CLI, the plugin can still build the
  offer summary, pain statements, query sets, and ranking framework
- without live Reddit scraping, it should say that live discovery is blocked
  instead of pretending the run happened

## How it works

1. Read skill-local memory notes for domain, URL, ICP, seed-pack, and run-ledger tuning.
2. Break the offer into pain primitives, trigger events, and buyer language.
3. Build short Reddit-native query families.
4. Run a bounded Apify search against `harshmaur/reddit-scraper`.
5. Normalize the dataset into thread-level goodput metrics and a ready-to-paste run-ledger row.
6. Rank threads, penalize self-promo and AI slop, and classify each thread into `direct_buyer`, `visibility_leverage`, or `discard`, then keep only `engage_now` or `discard`.
7. Draft casual, thread-specific public replies when asked.

## Retrieval contract

- The returned queue is `raw surfaces -> engage_now -> discard`.
- There is no watchlist or maybe-later result bucket in the published contract.
- Broad all-Reddit search is exploratory only and is not the default goodput
  path.
- For real use, prefer bounded communities, seeded surfaces, or named audience
  clusters.

## Usage

Example prompts:

- Find Reddit signal for `https://audienti.com/exo` and show the best threads.
- Turn this offer into Reddit search queries, findings, and reply drafts.
- Find real Reddit conversations where this ICP is complaining about the problem.
- Run Reddit signal discovery for this offer and tell me what to write back.

## Repository layout

```text
.codex-plugin/plugin.json
.claude-plugin/plugin.json
skills/reddit-pain-discovery/SKILL.md
skills/reddit-pain-discovery/assets/finding-template.md
skills/reddit-pain-discovery/references/apify-reddit-scraper.md
skills/reddit-pain-discovery/references/pain-query-framework.md
skills/reddit-pain-discovery/references/reddit-engagement-rubric.md
skills/reddit-pain-discovery/references/reply-modes.md
skills/reddit-pain-discovery/scripts/normalize_apify_search_results.py
skills/reddit-pain-discovery/scripts/resolve_memory.py
skills/reddit-pain-discovery/memory/README.md
skills/reddit-pain-discovery/memory/lessons.md
skills/reddit-pain-discovery/memory/domains/
skills/reddit-pain-discovery/memory/icps/
skills/reddit-pain-discovery/memory/run_ledgers/
skills/reddit-pain-discovery/memory/seed_packs/
skills/reddit-pain-discovery/memory/urls/
skills/reddit-pain-discovery/memory/templates/
```

## Marketplace source

Marketplace entries can reference this repository:

```text
https://github.com/audienti/reddit-pain-finder.git
```

For the Audienti Codex marketplace catalog, the entry should use:

```json
{
  "name": "reddit-pain-finder",
  "source": {
    "source": "url",
    "url": "https://github.com/audienti/reddit-pain-finder.git"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Sales"
}
```

## Validation

```bash
python3 /Users/williamflanagan/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 /Users/williamflanagan/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/reddit-pain-discovery
python3 skills/reddit-pain-discovery/scripts/resolve_memory.py --url https://example.com --icp "AI founders"
python3 skills/reddit-pain-discovery/scripts/normalize_apify_search_results.py --input sample.json
```

The memory resolver command is a read-only smoke test when run without
`--scaffold`.

## License

Copyright (c) 2026 OMALab, Inc. All rights reserved.

This plugin is not open source. Wholesale copying, redistribution, resale, or
publication of substantial portions requires prior written permission. Fair use,
short quotations, references, summaries, links, and commentary are not limited.
Attribution to OMALab, Inc. and a link to this repository are requested when
quoting or referencing the work.
