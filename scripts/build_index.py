#!/usr/bin/env python3
"""Rebuild issues/index.json from issues/*.json, and write newsletters/<date>.md
for any issue that has no Markdown copy yet.

Usage (from the repo root):  python3 scripts/build_index.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ISSUES = ROOT / "issues"
NEWS = ROOT / "newsletters"


def to_markdown(iss):
    out = [f"# {iss['title']}", "", f"Coverage: {iss.get('window', '')}", ""]
    if iss.get("note"):
        out += [f"*Editorial note: {iss['note']}*", ""]
    out += ["## This week in 60 seconds", ""]
    out += [f"- {x['t']}" for x in iss.get("sixty", [])] + [""]
    for sec in iss.get("sections", []):
        out += [f"## {sec['n']}. {sec['title']}", ""]
        for it in sec.get("items", []):
            links = ", ".join(f"[{l['t']}]({l['u']})" for l in it.get("l", []))
            out += [f"**{it['h']}** ({it.get('date', '')}). {it['s']} ({links})", "",
                    f"*Why it matters for us:* {it['w']}", ""]
        if sec.get("quiet"):
            out += [sec["quiet"], ""]
    if iss.get("deadlines"):
        out += ["## Deadlines & dates to watch", "", "| Date | Item | Owner hint |", "| --- | --- | --- |"]
        out += [f"| {d['label']} | {d['item']} | {d['owner']} |" for d in iss["deadlines"]] + [""]
    if iss.get("agenda"):
        out += ["## Suggested SAB / team discussion points", ""]
        out += [f"{i}. **{a['b']}** {a['p']}" for i, a in enumerate(iss["agenda"], 1)] + [""]
    return "\n".join(out)


def main():
    NEWS.mkdir(exist_ok=True)
    entries = []
    for f in sorted(ISSUES.glob("*.json")):
        if f.name == "index.json":
            continue
        iss = json.loads(f.read_text(encoding="utf-8"))
        entries.append({"date": iss["date"], "issueNo": iss.get("issueNo"), "title": iss.get("title")})
        md = NEWS / f"{iss['date']}.md"
        if not md.exists():
            md.write_text(to_markdown(iss), encoding="utf-8")
    entries.sort(key=lambda e: e["date"], reverse=True)
    (ISSUES / "index.json").write_text(
        json.dumps({"latest": entries[0]["date"] if entries else None, "issues": entries},
                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(entries)} issue(s) indexed; latest = {entries[0]['date'] if entries else '-'}")


if __name__ == "__main__":
    main()
