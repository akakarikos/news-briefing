# Fintech & Architecture Briefing — library

Weekly briefing on European banking regulation, payments, security, solution architecture and enterprise AI, written for a Greek bank's architecture team.

**Dashboard:** https://akakarikos.github.io/news-briefing/

- `index.html` — the library: latest issue, archive, search, favorites and read-later. Marks are saved in the browser and, with **Sync** on, in a secret GitHub Gist so they follow you across devices (needs a classic token with only the `gist` scope, entered once per device).
- `issues/<YYYY-MM-DD>.json` — one file per issue (the dashboard's data).
- `issues/index.json` — list of issues, rebuilt by `scripts/build_index.py`.
- `newsletters/<YYYY-MM-DD>.md` — Markdown copy of each issue.

Deep links: `#latest`, `#archive`, `#favorites`, `#read-later`, `#issue-2026-11-03`, `#issue-2026-11-03--<item-id>`.

## Adding an issue

1. Save the issue as `issues/<YYYY-MM-DD>.json` (same shape as the existing files).
2. Optionally save its Markdown copy as `newsletters/<YYYY-MM-DD>.md`.
3. Run `python3 scripts/build_index.py`, commit and push. GitHub Pages republishes within a minute or two.
