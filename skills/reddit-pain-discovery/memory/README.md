# Skill Memory

This folder stores reusable tuning learned from live runs.

Use it so the skill does not rediscover the same query drift patterns every time.

## Memory Types

- `lessons.md`
  Use for cross-run rules that should shape all future executions of the skill.
  This is the closest match to Recursive Drift's self-improvement loop.

- `domains/`
  Use when the tuning is reusable across the whole company or domain.
  Example: `actico.com` is broadly about compliance, credit risk, and decisioning in regulated finance, so its drift patterns and winning query language belong in a domain note.

- `urls/`
  Use when the tuning is specific to one page, wedge, or path.
  Example: `audienti.com/exo` is one offer on `audienti.com`, so the best query language for `/exo` belongs in a URL note.

## Naming

- Domain note:
  Lowercase host with dots replaced by dashes.
  Example: `actico.com` -> `domains/actico-com.md`

- URL note:
  Start with the normalized host, then `__`, then the path with leading and trailing slashes removed and remaining slashes replaced by `--`.
  Example: `https://audienti.com/exo` -> `urls/audienti-com__exo.md`

If a URL has no path or only `/`, use only the domain note.

## Helper Script

Use:

```bash
python3 scripts/resolve_memory.py --url "https://example.com/path" --scaffold
```

The script:

- normalizes the host and path
- computes the domain note path
- computes the URL note path when relevant
- creates missing notes from templates when `--scaffold` is passed
- prints a JSON payload the agent can use directly

## What To Record

Each note should capture:

- offer or domain summary
- ICP framing that actually helped
- winning query patterns
- losing query patterns
- productive communities
- noisy communities or content types
- exclusion cues and slop cues
- open questions or next tests

`lessons.md` should capture:

- what happened
- the rule that should persist
- a short active-rules list distilled from past entries

## Operating Rule

These notes are priors, not truth.

If fresh live results contradict a note, update the note.
