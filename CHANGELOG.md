# Changelog

## 0.1.2 - 2026-06-20

- Renamed the user-facing plugin surface to Reddit Signal Finder.
- Tightened the publish contract to `raw surfaces -> engage_now -> discard`.
- Documented bounded-community and seeded-surface Reddit discovery as the
  default goodput path instead of broad all-Reddit search.

## 0.1.1 - 2026-06-15

- Added explicit reply modes for vent threads, operator-advice threads, diagnostic threads, and recommendation threads.
- Added a disengagement rule for AI or shill accusations so the skill stops escalating bad thread dynamics.
- Added a new lesson about vent-thread mismatch and over-structured replies.

## 0.1.0 - 2026-06-15

- Packaged Reddit Pain Finder as a standalone Codex and Claude Code plugin.
- Moved the tuned `reddit-pain-discovery` skill into `skills/reddit-pain-discovery/`.
- Included memory notes, engagement rubric, query framework, output template, and memory resolver script.
- Hardened the Apify runtime contract so the skill can use either the Apify tool surface or an authenticated `apify` CLI.
- Added proprietary copyright and attribution license notice.
