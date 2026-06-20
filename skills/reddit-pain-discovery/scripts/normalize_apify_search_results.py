#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


FIRST_PERSON_RE = re.compile(r"\b(i|we|my|our|me|us)\b", re.IGNORECASE)
SECOND_PERSON_RE = re.compile(r"\b(you|your|yours)\b", re.IGNORECASE)
REQUEST_RE = re.compile(
    r"\b(anyone|looking for|need to|need help|recommend|recommendation|what are you using|how do you|struggling|stuck|frustrated|painful)\b",
    re.IGNORECASE,
)
PAIN_RE = re.compile(
    r"\b(broken|manual|slow|delay|late|outage|issue|problem|risk|backlog|renewal|vendor|support|escalation|false positive|approval|review)\b",
    re.IGNORECASE,
)
STRATEGIC_RE = re.compile(
    r"\b(evaluating|shortlist|compare|comparison|governance|budget|renewal|roadmap|planning|migration|transition|standardize)\b",
    re.IGNORECASE,
)
PROMO_RE = re.compile(
    r"\b(book a demo|dm me|message me|sign up|join our|join my|newsletter|webinar|launching|launched|promo code|discount|free trial|check out|i'?m building|i am building|working on a|working on an|exploring an ai-based|would really value feedback|get some input from|curious what this community thinks|research company|potential risks or gaps|input from others|help you\?)\b",
    re.IGNORECASE,
)
HIRING_RE = re.compile(
    r"\b(hiring|job opening|open role|open position|recruiter|apply now|resume|job posting|salary|position \$)\b",
    re.IGNORECASE,
)
AI_SLOP_RE = re.compile(
    r"\b(10x|game changer|thought leader|vibe coded|vibecoded|agentic|revolutionize|unlock|disrupt|guru)\b",
    re.IGNORECASE,
)
BUSINESS_CONTEXT_RE = re.compile(
    r"\b(qbr|scorecard|renewal|renewals|procurement|purchasing|supplier|suppliers|fulfillment|support portal|support case|support cases|ticket|tickets|escalation|escalations|contract|contracts|compliance|budget|approval|approvals|purchase order|purchase orders|rfp|operations|it team|sysadmin|infrastructure|colo|colocation|data center|credit risk|underwriting|aml|risk team|vendor management|vendor governance|vendor performance)\b",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://\S+")
QUERY_TOKEN_RE = re.compile(r"[a-z0-9]{3,}")
QUERY_STOPWORDS = {
    "lang",
    "with",
    "this",
    "that",
    "using",
    "anyone",
    "what",
    "where",
    "when",
    "week",
    "month",
    "year",
    "hour",
    "hours",
    "days",
    "latest",
    "search",
    "posts",
    "comments",
}
BROAD_QUERY_TOKENS = {
    "vendor",
    "vendors",
    "supplier",
    "suppliers",
    "metrics",
    "spreadsheet",
    "scorecard",
    "tracking",
    "performance",
    "cases",
    "management",
    "tool",
    "tools",
    "software",
    "system",
    "systems",
    "platform",
    "platforms",
    "support",
    "governance",
    "review",
    "leverage",
    "accountability",
    "scattered",
}


def load_items(path: str | None) -> list[dict]:
    if path:
        payload = Path(path).read_text()
    else:
        payload = sys.stdin.read()
    data = json.loads(payload or "[]")
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array of Apify dataset items.")
    return [item for item in data if isinstance(item, dict)]


def pick(*values):
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return None


def nested_value(item: dict, *paths: tuple[str, ...]):
    for path in paths:
        current = item
        ok = True
        for key in path:
            if not isinstance(current, dict) or key not in current:
                ok = False
                break
            current = current[key]
        if ok and current not in (None, "", [], {}):
            return current
    return None


def clean_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        value = json.dumps(value, sort_keys=True)
    return str(value).strip()


def combine_text(parts: list[str]) -> str:
    cleaned = []
    seen = set()
    for part in parts:
        text = clean_text(part)
        if not text:
            continue
        if text in seen:
            continue
        seen.add(text)
        cleaned.append(text)
    return "\n\n".join(cleaned)


def extract_query_label(item: dict) -> str | None:
    value = pick(
        item.get("searchTerm"),
        item.get("searchTerms"),
        item.get("query"),
        item.get("_query_file"),
        nested_value(item, ("metadata", "query")),
    )
    if isinstance(value, list):
        return " | ".join(clean_text(part) for part in value if clean_text(part))
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True)
    text = clean_text(value)
    return text or None


def extract_comments_from_list(value) -> list[dict]:
    if not isinstance(value, list):
        return []
    comments = []
    for comment in value:
        if isinstance(comment, dict):
            comments.append(comment)
    return comments


def extract_comment_rows(item: dict) -> list[dict]:
    embedded_comments = []
    for candidate in (
        item.get("comments"),
        item.get("postComments"),
        nested_value(item, ("data", "comments")),
    ):
        embedded_comments.extend(extract_comments_from_list(candidate))

    comment_body = pick(
        item.get("body"),
        item.get("comment"),
        item.get("commentBody"),
        item.get("text"),
    )
    if clean_text(comment_body) and not clean_text(item.get("title")):
        embedded_comments.append(
            {
                "id": pick(item.get("commentId"), item.get("id")),
                "author": pick(item.get("author"), item.get("username")),
                "body": comment_body,
            }
        )

    return embedded_comments


def extract_author_name(item: dict) -> str | None:
    value = pick(
        item.get("author"),
        item.get("authorName"),
        item.get("username"),
        nested_value(item, ("author", "name")),
    )
    text = clean_text(value)
    return text or None


def extract_thread_key(item: dict) -> str:
    value = pick(
        item.get("postId"),
        item.get("id"),
        item.get("permalink"),
        item.get("url"),
        item.get("link"),
        item.get("postUrl"),
    )
    text = clean_text(value)
    return text or "unknown-thread"


def extract_root_text(item: dict) -> str:
    return combine_text(
        [
            item.get("title"),
            item.get("selftext"),
            item.get("selfText"),
            item.get("body"),
            item.get("text"),
            item.get("content"),
            item.get("postText"),
        ]
    )


def detect_item_kind(item: dict, root_text: str, comments: list[dict]) -> str:
    if clean_text(item.get("title")) or clean_text(item.get("selftext")) or clean_text(item.get("permalink")):
        return "post"
    if comments or root_text:
        return "comment"
    return "unknown"


def speaker_perspective(text: str) -> str:
    if FIRST_PERSON_RE.search(text):
        return "first_person_self_report"
    if SECOND_PERSON_RE.search(text):
        return "second_person_advice"
    return "third_person_commentary"


def is_substantive_text(text: str) -> bool:
    normalized = clean_text(URL_RE.sub("", text))
    if len(normalized) < 40:
        return False
    return len(normalized.split()) >= 8


def query_label_match(text_tokens: set[str], label: str) -> bool:
    normalized = clean_text(label).lower()
    if not normalized:
        return True
    if "http://" in normalized or "https://" in normalized:
        return True
    anchor_tokens = {
        token
        for token in QUERY_TOKEN_RE.findall(normalized)
        if token not in QUERY_STOPWORDS
    }
    if not anchor_tokens:
        return True

    matched_tokens = anchor_tokens & text_tokens
    specific_tokens = anchor_tokens - BROAD_QUERY_TOKENS
    if specific_tokens:
        return bool(specific_tokens & text_tokens)
    minimum_overlap = 3 if len(anchor_tokens) >= 3 else len(anchor_tokens)
    return len(matched_tokens) >= minimum_overlap


def query_anchor_match(text: str, labels: list[str]) -> bool:
    if not labels:
        return True
    text_tokens = set(QUERY_TOKEN_RE.findall(clean_text(text).lower()))
    return any(query_label_match(text_tokens, label) for label in labels)


def classify_commercial_path(
    *,
    request_signal: bool,
    pain_signal: bool,
    strategic_signal: bool,
    root_operator_signal: bool,
    has_external_substantive_discussion: bool,
    promotional: bool,
    hiring: bool,
    ai_slop: bool,
) -> str:
    if promotional or hiring or ai_slop or not has_external_substantive_discussion:
        return "discard"
    if request_signal or pain_signal or strategic_signal or root_operator_signal:
        return "direct_buyer"
    return "visibility_leverage"


def choose_action_type(
    *,
    commercial_path: str,
    anchor_match: bool,
    business_context: bool,
    root_operator_signal: bool,
    external_substantive_comment_count: int,
) -> str:
    if commercial_path == "discard" or not anchor_match or not business_context:
        return "discard"
    if not root_operator_signal and external_substantive_comment_count == 0:
        return "discard"
    return "engage_now"


def analyze_text(text: str, perspective: str) -> dict:
    request_signal = bool(REQUEST_RE.search(text))
    pain_signal = bool(PAIN_RE.search(text))
    strategic_signal = bool(STRATEGIC_RE.search(text))
    promo = bool(PROMO_RE.search(text))
    hiring = bool(HIRING_RE.search(text))
    ai_slop = bool(AI_SLOP_RE.search(text)) or text.count("#") >= 5
    # ponytail: blunt business-shape gate; widen only when real false negatives show up.
    business_context = bool(BUSINESS_CONTEXT_RE.search(text))
    visibility_only = (
        (
            perspective == "second_person_advice"
            or perspective == "third_person_commentary"
        )
        and not request_signal
        and not pain_signal
        and not strategic_signal
    )
    root_operator_signal = business_context and is_substantive_text(text) and (
        request_signal
        or strategic_signal
        or (pain_signal and perspective == "first_person_self_report")
    )
    return {
        "businessContext": business_context,
        "requestSignal": request_signal,
        "painSignal": pain_signal,
        "strategicSignal": strategic_signal,
        "isPromotional": promo,
        "isHiring": hiring,
        "isAiSlopLikely": ai_slop,
        "isVisibilityOnly": visibility_only,
        "rootOperatorSignal": root_operator_signal,
    }


def normalize_comment(comment: dict, thread_author: str | None) -> dict:
    author = clean_text(pick(comment.get("author"), comment.get("authorName"), comment.get("username"))) or None
    text = combine_text([comment.get("body"), comment.get("text"), comment.get("content")])
    external = bool(author and thread_author and author.lower() != thread_author.lower())
    substantive = is_substantive_text(text)
    return {
        "id": clean_text(pick(comment.get("id"), comment.get("commentId"))) or None,
        "author": author,
        "text": text,
        "isExternal": external,
        "isSubstantive": substantive,
    }


def failure_mode(flags: dict, external_count: int) -> str:
    if not flags["businessContext"]:
        return "off_topic_surface"
    if flags["isPromotional"] or flags["isHiring"]:
        return "promo_or_hiring"
    if flags["isAiSlopLikely"]:
        return "ai_slop_or_low_substance"
    if flags["isVisibilityOnly"]:
        return "visibility_without_goodput"
    if external_count == 0 and not flags["rootOperatorSignal"]:
        return "no_substantive_discussion"
    return "goodput_candidate"


def build_thread(item: dict) -> dict:
    root_text = extract_root_text(item)
    comments = extract_comment_rows(item)
    kind = detect_item_kind(item, root_text, comments)
    return {
        "threadKey": extract_thread_key(item),
        "itemKind": kind,
        "sourceQueries": [query for query in [extract_query_label(item)] if query],
        "url": clean_text(pick(item.get("url"), item.get("permalink"), item.get("link"), item.get("postUrl"))) or None,
        "subreddit": clean_text(
            pick(
                item.get("subreddit"),
                item.get("subredditName"),
                nested_value(item, ("subreddit", "name")),
            )
        )
        or None,
        "title": clean_text(item.get("title")) or None,
        "author": extract_author_name(item),
        "createdAt": clean_text(pick(item.get("createdAt"), item.get("created"), item.get("date"))) or None,
        "text": root_text,
        "comments": comments,
        "rawRows": [item],
    }


def merge_threads(existing: dict, incoming: dict) -> dict:
    if not existing:
        return incoming

    existing["sourceQueries"] = sorted(set(existing["sourceQueries"] + incoming["sourceQueries"]))
    existing["rawRows"].extend(incoming["rawRows"])

    if incoming["itemKind"] == "post" and existing["itemKind"] != "post":
        for key in ("itemKind", "url", "subreddit", "title", "author", "createdAt", "text"):
            existing[key] = incoming[key]
    elif len(incoming["text"]) > len(existing["text"]):
        for key in ("url", "subreddit", "title", "author", "createdAt", "text"):
            if incoming[key]:
                existing[key] = incoming[key]

    existing["comments"].extend(incoming["comments"])
    return existing


def analyze_thread(thread: dict) -> dict:
    perspective = speaker_perspective(thread["text"])
    flags = analyze_text(thread["text"], perspective)
    normalized_comments = []
    seen_comment_keys = set()
    external_substantive_comment_count = 0
    for comment in thread["comments"]:
        normalized_comment = normalize_comment(comment, thread.get("author"))
        key = normalized_comment["id"] or normalized_comment["text"][:120]
        if key in seen_comment_keys:
            continue
        seen_comment_keys.add(key)
        normalized_comments.append(normalized_comment)
        if normalized_comment["isExternal"] and normalized_comment["isSubstantive"]:
            external_substantive_comment_count += 1

    credible_root_discussion = (
        flags["rootOperatorSignal"]
        and not flags["isPromotional"]
        and not flags["isHiring"]
        and not flags["isAiSlopLikely"]
    )
    has_external_substantive_discussion = (
        credible_root_discussion or external_substantive_comment_count > 0
    )
    anchor_match = query_anchor_match(thread["text"], thread["sourceQueries"])
    commercial_path = classify_commercial_path(
        request_signal=flags["requestSignal"],
        pain_signal=flags["painSignal"],
        strategic_signal=flags["strategicSignal"],
        root_operator_signal=flags["rootOperatorSignal"],
        has_external_substantive_discussion=has_external_substantive_discussion,
        promotional=flags["isPromotional"],
        hiring=flags["isHiring"],
        ai_slop=flags["isAiSlopLikely"],
    )
    action_type = choose_action_type(
        commercial_path=commercial_path,
        anchor_match=anchor_match,
        business_context=flags["businessContext"],
        root_operator_signal=flags["rootOperatorSignal"],
        external_substantive_comment_count=external_substantive_comment_count,
    )
    goodput_candidate = action_type == "engage_now"
    thread["comments"] = normalized_comments
    thread["analysis"] = {
        "speakerPerspectiveHint": perspective,
        "queryAnchorMatch": anchor_match,
        "hasExternalSubstantiveDiscussion": has_external_substantive_discussion,
        "externalSubstantiveCommentCount": external_substantive_comment_count,
        "commercialClass": commercial_path,
        "actionType": action_type,
        "goodputCandidate": goodput_candidate,
        "visibilityOnly": commercial_path == "visibility_leverage",
        "primaryFailureMode": failure_mode(flags, external_substantive_comment_count),
        **flags,
    }
    return thread


def build_run_ledger(summary: dict, tuning: dict) -> dict:
    query_count = len(summary["queryCounts"])
    scraped_thread_count = summary["scrapedThreadCount"]
    goodput_count = summary["goodputOpportunityCount"]
    visibility_only_count = summary["visibilityOnlyCount"]
    external_discussion_count = summary["externalSubstantiveDiscussionCount"]
    goodput_rate = round(goodput_count / scraped_thread_count, 3) if scraped_thread_count else 0.0
    return {
        "queryCount": query_count,
        "seedCount": 0,
        "scrapedThreadCount": scraped_thread_count,
        "externalSubstantiveDiscussionCount": external_discussion_count,
        "goodputOpportunityCount": goodput_count,
        "postedEngagementCount": 0,
        "goodputRate": goodput_rate,
        "visibilityOnlyCount": visibility_only_count,
        "primaryFailureMode": tuning["primaryFailureMode"],
        "markdownRow": (
            "| YYYY-MM-DD | "
            f"{query_count} | 0 | {scraped_thread_count} | {external_discussion_count} | "
            f"{goodput_count} | 0 | {tuning['primaryFailureMode']} | replace with live notes |"
        ),
    }


def normalize(items: list[dict]) -> dict:
    query_counts = Counter()
    raw_kind_counts = Counter()
    threads_by_key: dict[str, dict] = {}

    for item in items:
        built = build_thread(item)
        raw_kind_counts[built["itemKind"]] += 1
        for label in built["sourceQueries"]:
            query_counts[label] += 1
        threads_by_key[built["threadKey"]] = merge_threads(threads_by_key.get(built["threadKey"]), built)

    threads = [analyze_thread(thread) for thread in threads_by_key.values()]
    failure_counts = Counter(thread["analysis"]["primaryFailureMode"] for thread in threads)

    summary = {
        "totalItems": len(items),
        "rawItemKindCounts": dict(raw_kind_counts),
        "queryCounts": dict(query_counts),
        "scrapedThreadCount": len(threads),
        "externalSubstantiveDiscussionCount": sum(
            1 for thread in threads if thread["analysis"]["hasExternalSubstantiveDiscussion"]
        ),
        "goodputOpportunityCount": sum(
            1 for thread in threads if thread["analysis"]["goodputCandidate"]
        ),
        "directBuyerCount": sum(
            1
            for thread in threads
            if thread["analysis"]["commercialClass"] == "direct_buyer"
            and thread["analysis"]["actionType"] == "engage_now"
        ),
        "visibilityLeverageCount": sum(
            1
            for thread in threads
            if thread["analysis"]["commercialClass"] == "visibility_leverage"
            and thread["analysis"]["actionType"] == "engage_now"
        ),
        "engageNowCount": sum(
            1 for thread in threads if thread["analysis"]["actionType"] == "engage_now"
        ),
        "deepenNowCount": 0,
        "discardCount": sum(
            1 for thread in threads if thread["analysis"]["actionType"] == "discard"
        ),
        "visibilityOnlyCount": sum(
            1 for thread in threads if thread["analysis"]["commercialClass"] == "visibility_leverage"
        ),
    }

    failure_only_counts = Counter(
        thread["analysis"]["primaryFailureMode"]
        for thread in threads
        if not thread["analysis"]["goodputCandidate"]
    )
    tuning = {
        "primaryFailureMode": (
            failure_only_counts.most_common(1)[0][0]
            if failure_only_counts
            else ("goodput_present" if summary["goodputOpportunityCount"] > 0 else "no_results")
        ),
        "stopLossTriggered": summary["goodputOpportunityCount"] == 0,
        "spendDecision": (
            "engage_and_track_replies"
            if summary["goodputOpportunityCount"] > 0
            else "retune_queries_or_communities"
        ),
    }

    return {
        "summary": summary,
        "tuning": tuning,
        "runLedger": build_run_ledger(summary, tuning),
        "threads": threads,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize Reddit scraper dataset items into a goodput-oriented thread summary."
    )
    parser.add_argument(
        "--input",
        help="Path to a JSON file containing dataset items. Reads stdin when omitted.",
    )
    args = parser.parse_args()

    items = load_items(args.input)
    print(json.dumps(normalize(items), indent=2))


if __name__ == "__main__":
    main()
