#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


SKILL_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = SKILL_DIR / "memory"
DOMAIN_DIR = MEMORY_DIR / "domains"
URL_DIR = MEMORY_DIR / "urls"
TEMPLATE_DIR = MEMORY_DIR / "templates"
DOMAIN_TEMPLATE = TEMPLATE_DIR / "domain-note-template.md"
URL_TEMPLATE = TEMPLATE_DIR / "url-note-template.md"


def normalize_host(host: str) -> str:
    host = host.lower().strip()
    if host.startswith("www."):
        host = host[4:]
    return host


def host_slug(host: str) -> str:
    return normalize_host(host).replace(".", "-")


def path_slug(path: str) -> str:
    trimmed = path.strip().strip("/")
    if not trimmed:
        return ""
    return trimmed.replace("/", "--")


def parse_target(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    if not parsed.scheme:
        parsed = urlparse(f"https://{url}")
    if not parsed.netloc:
        raise ValueError(f"Could not parse host from URL: {url}")
    return normalize_host(parsed.netloc), parsed.path or "/"


def write_from_template(target: Path, template: Path, title: str) -> None:
    content = template.read_text()
    content = content.replace("# example-com__path", f"# {title}")
    content = content.replace("# example-com", f"# {title}")
    target.write_text(content)


def resolve_paths(url: str) -> dict:
    host, path = parse_target(url)
    host_key = host_slug(host)
    path_key = path_slug(path)

    domain_note = DOMAIN_DIR / f"{host_key}.md"
    url_note = None
    if path_key:
        url_note = URL_DIR / f"{host_key}__{path_key}.md"

    return {
        "input_url": url,
        "normalized_host": host,
        "normalized_path": path if path else "/",
        "domain_key": host_key,
        "url_key": f"{host_key}__{path_key}" if path_key else None,
        "domain_note": str(domain_note),
        "url_note": str(url_note) if url_note else None,
        "domain_exists": domain_note.exists(),
        "url_exists": url_note.exists() if url_note else None,
    }


def scaffold(paths: dict) -> dict:
    created = []

    domain_note = Path(paths["domain_note"])
    if not domain_note.exists():
        write_from_template(domain_note, DOMAIN_TEMPLATE, paths["domain_key"])
        created.append(str(domain_note))
        paths["domain_exists"] = True

    if paths["url_note"]:
        url_note = Path(paths["url_note"])
        if not url_note.exists():
            write_from_template(url_note, URL_TEMPLATE, paths["url_key"])
            created.append(str(url_note))
            paths["url_exists"] = True

    paths["created"] = created
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve and optionally scaffold skill memory notes for a URL.")
    parser.add_argument("--url", required=True, help="Offer URL or host/path to resolve.")
    parser.add_argument("--scaffold", action="store_true", help="Create missing note files from templates.")
    args = parser.parse_args()

    paths = resolve_paths(args.url)
    if args.scaffold:
        paths = scaffold(paths)
    else:
        paths["created"] = []

    print(json.dumps(paths, indent=2))


if __name__ == "__main__":
    main()
