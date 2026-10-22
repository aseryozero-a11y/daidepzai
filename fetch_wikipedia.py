#!/usr/bin/env python3
"""Fetch the Wikipedia "featured" feed and store a daily snapshot.

This politely uses the public Wikimedia REST API for a *bounded* amount of
content (today's featured article, most-read pages, image of the day, ...)
instead of crawling the whole of Wikipedia.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

REPO_URL = "https://github.com/aseryozero-a11y/daidepzai"
USER_AGENT = os.environ.get(
    "WIKI_USER_AGENT",
    f"thangxinhzai/1.0 ({REPO_URL}; contact: 346338795+aseryozero-a11y@users.noreply.github.com)",
)
LANG = os.environ.get("WIKI_LANG", "en")
FEED = "https://api.wikimedia.org/feed/v1/wikipedia/{lang}/featured/{y}/{m:02d}/{d:02d}"
OUT_DIR = Path(__file__).resolve().parent / "data"
MOST_READ_COUNT = 10
ON_THIS_DAY_COUNT = 10


def fetch_feed(day: datetime) -> dict:
    url = FEED.format(lang=LANG, y=day.year, m=day.month, d=day.day)
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=30) as resp:
        return json.load(resp)


def digest(feed: dict, day: datetime) -> dict:
    """Keep only a compact, useful subset of the feed to avoid repo bloat."""
    tfa = feed.get("tfa") or {}
    image = feed.get("image") or {}
    most_read = (feed.get("mostread") or {}).get("articles") or []
    on_this_day = feed.get("onthisday") or []
    return {
        "lang": LANG,
        "date": f"{day:%Y-%m-%d}",
        "featured_article": {
            "title": (tfa.get("titles") or {}).get("normalized"),
            "extract": (tfa.get("extract") or "").strip()[:2000] or None,
        },
        "image_of_the_day": image.get("title"),
        "most_read": [
            a.get("title") for a in most_read[:MOST_READ_COUNT] if a.get("title")
        ],
        "on_this_day": [
            {"year": e.get("year"), "text": e.get("text")}
            for e in on_this_day[:ON_THIS_DAY_COUNT]
            if e.get("text")
        ],
    }


def summarize(data: dict) -> str:
    lines = []
    if data["featured_article"]["title"]:
        lines.append(f"Featured article: {data['featured_article']['title']}")
    if data["image_of_the_day"]:
        lines.append(f"Image of the day: {data['image_of_the_day']}")
    if data["most_read"]:
        lines.append(f"Most read: {', '.join(data['most_read'][:5])}")
    return "\n".join(lines) or "No featured content returned."


def main() -> int:
    day = datetime.now(timezone.utc)
    data = digest(fetch_feed(day), day)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # The daily feed is stable, so this file only changes once per day;
    # git history keeps the older versions.
    (OUT_DIR / "latest.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"Fetched {LANG} featured feed for {day:%Y-%m-%d} at {day:%H:%M:%S} UTC")
    print(summarize(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
