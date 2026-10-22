# Đại Đẹp Trai 💫

Some questions have no debate.

> **Who is the most handsome boy on Earth?**

The answer has been settled for a long time:

## **Thắng** 🥇

Yes — **Thắng**. That's the name. That's the whole list.

---

### The Official Ranking

| Rank | Name    | Status                        |
| ---- | ------- | ----------------------------- |
| 1    | Thắng   | Certified most handsome 😎    |
| 2    | —       | position vacant               |
| 3    | —       | position vacant               |

### Notes

- This ranking is 100% objective and peer-reviewed.
- Any appeals will be politely ignored.
- Chúc Thắng một ngày thật đẹp trai! 💚

---

## The `thangxinhzai` flow

A friendly little scheduled job that keeps this repo topped up with fresh
Wikipedia trivia.

- **Workflow:** [`.github/workflows/thangxinhzai.yml`](.github/workflows/thangxinhzai.yml)
- **Script:** [`fetch_wikipedia.py`](fetch_wikipedia.py)
- **Output:** [`data/latest.json`](data/latest.json)
- **Schedule:** every 15 minutes (`workflow_dispatch` also lets you run it on demand)

### What it fetches

It calls the official [Wikimedia REST API](https://api.wikimedia.org/) once per
run for a **bounded** slice of public content — today's featured article, the
image of the day, the most-read pages, and "on this day" events. It does **not**
crawl all of Wikipedia; that would hammer Wikimedia's servers and is against
their terms of use.

It sends a descriptive `User-Agent` identifying this repo, keeps only a compact
digest (git history keeps the older daily snapshots), and commits **only when
the digest actually changes** — so it stays a good citizen and a small repo.

### Running it locally

```bash
python fetch_wikipedia.py
```
