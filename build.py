#!/usr/bin/env python3
"""Build portfolio.html from PORTFOLIO.md. Standard library only.

Usage: python3 build.py
Reads PORTFOLIO.md and writes portfolio.html plus one page per project in case-studies/. Image paths stay relative,
so the folder can be zipped and moved anywhere.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "PORTFOLIO.md"
OUT = ROOT / "portfolio.html"
CASES = ROOT / "case-studies"
PRIORITIES = ["P1", "P2", "P3"]
SECTIONS = {"context", "problem", "process", "solution", "outcome", "learnings", "metrics", "screens", "to fill in"}


def kv(line):
    m = re.match(r"^-?\s*([a-z_]+):\s*(.*)$", line.strip())
    return (m.group(1), m.group(2).strip()) if m else None


def parse(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    head, *blocks = re.split(r"^## ", text, flags=re.M)
    profile = {}
    for line in head.splitlines():
        if line.startswith("# "):
            profile["title"] = line[2:].strip()
        elif (pair := kv(line)):
            profile[pair[0]] = pair[1]
    projects = []
    for block in blocks:
        title, _, body = block.partition("\n")
        parts = re.split(r"^### ", body, flags=re.M)
        project = {"title": title.strip(), "sections": {}}
        for line in parts[0].splitlines():
            if (pair := kv(line)):
                project[pair[0]] = pair[1]
        for part in parts[1:]:
            name, _, content = part.partition("\n")
            name = name.strip().lower()
            if name in SECTIONS:
                project["sections"][name] = content.strip()
        projects.append(project)
    return profile, projects


def esc(s):
    return html.escape(s, quote=True)


def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\[(.+?)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)


def rich(text):
    out, bullets = [], []

    def flush():
        if bullets:
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in bullets) + "</ul>")
            bullets.clear()

    for para in re.split(r"\n\s*\n", text.strip()):
        lines = [l.strip() for l in para.splitlines() if l.strip()]
        if lines and all(l.startswith("- ") for l in lines):
            bullets.extend(l[2:] for l in lines)
            flush()
        elif lines:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return "".join(out)


def pairs(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- "):
            left, _, right = line[2:].partition("|")
            rows.append((left.strip(), right.strip()))
    return rows


def csv(value):
    return [v.strip() for v in value.split(",") if v.strip()]


def screens_html(p, pid):
    shots = pairs(p["sections"].get("screens", ""))
    main = (
        f'<div class="stage"><img id="{pid}-main" src="{esc(shots[0][0])}" alt="{esc(shots[0][1] or p["title"])}">'
        f'<span class="cap" id="{pid}-cap">{esc(shots[0][1])}</span></div>'
    )
    if len(shots) == 1:
        return main
    thumbs = "".join(
        f'<button class="thumb{" on" if i == 0 else ""}" data-target="{pid}" data-src="{esc(src)}" '
        f'data-cap="{esc(cap)}" aria-label="{esc(cap or "Screen " + str(i + 1))}">'
        f'<img src="{esc(src)}" alt="" loading="lazy"></button>'
        for i, (src, cap) in enumerate(shots)
    )
    return main + f'<div class="thumbs">{thumbs}</div>'


def project_html(p, idx):
    pid = f"p{idx}"
    prio = p.get("priority", "P3")
    tags = "".join(f'<span class="pill">{esc(t)}</span>' for t in csv(p.get("tags", "")))
    tools = " · ".join(esc(t) for t in csv(p.get("tools", "")))
    metrics = pairs(p["sections"].get("metrics", ""))
    metrics_html = (
        '<div class="metrics">'
        + "".join(f'<div><b>{esc(v)}</b><small>{esc(l)}</small></div>' for v, l in metrics)
        + "</div>"
        if metrics
        else ""
    )
    status = f'<span class="pill status"><i></i>{esc(p["status"])}</span>' if p.get("status") else ""
    outcome = p["sections"].get("outcome", "")
    outcome_html = f'<div class="outcome"><h4>Outcome</h4>{rich(outcome)}</div>' if outcome else ""
    context = p["sections"].get("context", "")
    has_shots = bool(pairs(p["sections"].get("screens", "")))
    shots = f'<div class="shots">{screens_html(p, pid)}</div>' if has_shots else ""
    return f"""
<article class="case {prio.lower()}{'' if has_shots else ' noshots'}" id="{esc(p.get('id', pid))}">
  <div class="copy">
    <div class="meta"><span class="pill">{esc(prio)}</span>{status}</div>
    <h3>{esc(p['title'])}</h3>
    <p class="lead">{inline(p.get('summary', ''))}</p>
    {metrics_html}
    <div class="body">{rich(context)}</div>
    {outcome_html}
    <div class="tags">{tags}</div>
    {f'<p class="tools">Tools · {tools}</p>' if tools else ''}
    <a class="more" href="case-studies/{esc(p.get('id', pid))}.html">Read case study <span>→</span></a>
  </div>
  {shots}
</article>"""


CSS = """
:root{--bg:#f1f1f1;--card:#fff;--ink:#0d0d0d;--mute:#9a9a9a;--line:#e8e8e8;--soft:#f6f6f6;--dark:#1b1b1b;--ok:#2fbf4a}
@media (prefers-color-scheme:dark){:root{--bg:#0e0e0e;--card:#1a1a1a;--ink:#f3f3f3;--mute:#7d7d7d;--line:#2a2a2a;--soft:#222;--dark:#000}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,"Helvetica Neue",-apple-system,"Segoe UI",Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding:48px 24px 80px}
h1,h2,h3,h4{letter-spacing:-.035em;line-height:1.05;margin:0}
.pill{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;padding:6px 12px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink)}
.pill.status i{width:7px;height:7px;border-radius:50%;background:var(--ok);display:inline-block}
.hero{display:grid;grid-template-columns:1.4fr 1fr;gap:32px;align-items:end;margin-bottom:32px}
.hero h1{font-size:clamp(40px,7vw,76px);margin-top:20px;font-weight:600}
.hero h1 span{color:var(--mute)}
.hero p{color:var(--mute);font-size:16px;max-width:380px;margin:0 0 6px auto}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:72px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:24px;padding:22px 24px;min-height:150px;display:flex;flex-direction:column;justify-content:space-between}
.stat b{font-size:56px;font-weight:500;letter-spacing:-.05em;line-height:1}
.stat small{color:var(--mute);font-size:13px}
.stat.dark{background:var(--dark);color:#fff;border-color:transparent;box-shadow:0 18px 40px -18px rgba(0,0,0,.45)}
.stat.dark small{color:#9d9d9d}
.section-head{display:flex;justify-content:space-between;align-items:end;margin:0 0 20px}
.section-head h2{font-size:clamp(28px,4vw,44px);font-weight:600}
.cases{display:flex;flex-direction:column;gap:20px}
.case{background:var(--card);border:1px solid var(--line);border-radius:32px;padding:20px;display:grid;grid-template-columns:1fr 1.05fr;gap:20px}
.case .copy{padding:20px 14px 14px 18px;display:flex;flex-direction:column;gap:18px}
.meta{display:flex;gap:8px;flex-wrap:wrap}
.case h3{font-size:clamp(26px,3.2vw,38px);font-weight:600}
.lead{font-size:17px;color:var(--ink);margin:0}
.body,.outcome{color:#6d6d6d;font-size:15px}
@media (prefers-color-scheme:dark){.body,.outcome{color:#a3a3a3}}
.body p,.outcome p{margin:0 0 10px}
.body ul,.outcome ul{margin:0;padding-left:18px}
.outcome h4{font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:var(--mute);margin-bottom:8px;font-weight:600}
.metrics{display:flex;gap:28px;flex-wrap:wrap;padding:6px 0}
.metrics b{display:block;font-size:34px;font-weight:500;letter-spacing:-.04em}
.metrics small{color:var(--mute);font-size:12px}
.tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:auto}
.tools{margin:0;color:var(--mute);font-size:13px}
.more{align-self:flex-start;display:inline-flex;gap:8px;align-items:center;background:var(--dark);color:#fff;text-decoration:none;font-size:13px;font-weight:500;padding:11px 18px;border-radius:999px;box-shadow:0 10px 24px -12px rgba(0,0,0,.5);transition:.2s}
.more:hover{transform:translateY(-1px)}
.shots{background:var(--soft);border-radius:24px;padding:18px;display:flex;flex-direction:column;gap:14px;min-height:420px}
.stage{flex:1;display:grid;place-items:center;position:relative;min-height:300px}
.stage img{width:min(100%,460px);aspect-ratio:1;object-fit:contain;filter:drop-shadow(0 30px 40px rgba(0,0,0,.18))}
.stage .cap{position:absolute;left:4px;bottom:0;font-size:13px;font-weight:600;letter-spacing:-.01em}
.stage.empty{color:var(--mute);font-size:14px}
.thumbs{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.thumb{width:64px;height:64px;padding:6px;border:1.5px solid transparent;border-radius:18px;background:var(--card);cursor:pointer;transition:.2s}
.thumb img{width:100%;height:100%;object-fit:contain;display:block}
.thumb.on,.thumb:hover{border-color:var(--ink)}
.case.p2 .shots{min-height:300px}
.case.p2 .stage{min-height:200px}
.case.p2 .stage img{width:min(100%,280px)}
.case.noshots{grid-template-columns:1fr}
.case.p3{grid-template-columns:1fr;padding:6px}
.case.p3 .shots,.case.p3 .body,.case.p3 .outcome{display:none}
footer{margin-top:64px;color:var(--mute);font-size:13px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media (max-width:860px){.hero,.case{grid-template-columns:1fr}.hero p{margin:0}.stats{grid-template-columns:1fr 1fr}.stat{min-height:120px}}
"""

JS = """
document.querySelectorAll('.thumb').forEach(function(b){b.addEventListener('click',function(){
  var id=b.dataset.target,img=document.getElementById(id+'-main'),cap=document.getElementById(id+'-cap');
  img.src=b.dataset.src;img.alt=b.dataset.cap;if(cap)cap.textContent=b.dataset.cap;
  b.parentNode.querySelectorAll('.thumb').forEach(function(t){t.classList.toggle('on',t===b)});
});});
"""


FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
)

CASE_CSS = """
.nav{display:flex;justify-content:space-between;align-items:center;margin-bottom:56px}
.nav a.pill{text-decoration:none;transition:.2s}
.nav a.pill:hover{border-color:var(--ink)}
.c-hero h1{font-size:clamp(38px,6.2vw,80px);font-weight:600;margin-top:22px;max-width:15ch}
.c-hero .sub{font-size:clamp(18px,2vw,24px);color:var(--mute);letter-spacing:-.02em;max-width:640px;margin:22px 0 0}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:44px 0 14px}
.fact{background:var(--card);border:1px solid var(--line);border-radius:24px;padding:20px 22px;display:flex;flex-direction:column;gap:18px;min-height:110px;justify-content:space-between}
.fact small{color:var(--mute);font-size:12px;text-transform:uppercase;letter-spacing:.05em;font-weight:600}
.fact b{font-size:19px;font-weight:500;letter-spacing:-.02em;line-height:1.25}
.gallery{background:var(--card);border:1px solid var(--line);border-radius:32px;padding:20px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,175px),1fr));gap:14px;align-items:start}
.tile{background:var(--soft);border:0;border-radius:24px;padding:26px 26px 20px;display:flex;flex-direction:column;gap:16px;cursor:zoom-in;font:inherit;color:inherit;text-align:left;transition:.25s}
.tile:hover{transform:translateY(-3px)}
.tile img{width:100%;height:auto;display:block;filter:drop-shadow(0 22px 26px rgba(0,0,0,.2))}
.tile span{font-size:14px;font-weight:600;letter-spacing:-.01em}
.story{margin-top:64px}
.row{display:grid;grid-template-columns:240px 1fr;gap:32px;padding:38px 0;border-top:1px solid var(--line)}
.row .pill{align-self:start;justify-self:start}
.row .txt{font-size:clamp(17px,1.6vw,20px);color:#5f5f5f;max-width:720px;letter-spacing:-.01em}
@media (prefers-color-scheme:dark){.row .txt{color:#a8a8a8}}
.row .txt p{margin:0 0 16px}.row .txt ul{margin:0 0 16px;padding-left:20px}.row .txt li{margin-bottom:6px}
.row.dark{background:var(--dark);border:0;border-radius:32px;padding:40px;margin:14px 0;color:#fff;box-shadow:0 24px 50px -24px rgba(0,0,0,.5)}
.row.dark .txt{color:#d4d4d4}
.row.dark .pill{background:transparent;color:#fff;border-color:#3a3a3a}
.cstats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:14px}
.next{margin-top:72px;background:var(--card);border:1px solid var(--line);border-radius:32px;padding:32px;display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}
.next small{color:var(--mute);font-size:12px;text-transform:uppercase;letter-spacing:.05em;font-weight:600}
.next h3{font-size:clamp(24px,3vw,34px);font-weight:600;margin-top:10px}
.next .more{align-self:center}
.lb{position:fixed;inset:0;background:rgba(0,0,0,.8);display:none;place-items:center;z-index:10;cursor:zoom-out;padding:24px}
.lb.on{display:grid}.lb img{max-width:min(92vw,900px);max-height:90vh;object-fit:contain}
@media (max-width:860px){.row{grid-template-columns:1fr;gap:16px;padding:28px 0}.row.dark{padding:28px 24px}}
@media (max-width:600px){.tiles{grid-template-columns:1fr 1fr}.tile{padding:16px 16px 14px}.facts{grid-template-columns:1fr 1fr}.fact{min-height:96px;padding:16px}}
"""

CASE_JS = """
var lb=document.getElementById('lb'),lbi=lb.querySelector('img');
document.querySelectorAll('.tile').forEach(function(t){t.addEventListener('click',function(){
  lbi.src=t.dataset.src;lbi.alt=t.dataset.cap;lb.classList.add('on');});});
lb.addEventListener('click',function(){lb.classList.remove('on');});
document.addEventListener('keydown',function(e){if(e.key==='Escape')lb.classList.remove('on');});
"""

STORY = [("context", "Context"), ("problem", "Problem"), ("process", "Process"),
         ("solution", "Solution"), ("outcome", "Outcome"), ("learnings", "Learnings")]


def ordered(projects):
    return sorted(
        projects, key=lambda p: PRIORITIES.index(p["priority"]) if p.get("priority") in PRIORITIES else len(PRIORITIES)
    )


def case_page(profile, p, projects):
    """One case study page. Lives in case-studies/, so asset paths get a ../ prefix."""
    role = p.get("role") or profile.get("role", "")
    company = profile.get("company", "")
    facts = [
        ("Role", role), ("Company", company), ("Tools", " · ".join(csv(p.get("tools", "")))),
        ("Status", p.get("status", "")), ("Timeline", p.get("timeline", "")), ("Team", p.get("team", "")),
    ]
    facts_html = "".join(f'<div class="fact"><small>{k}</small><b>{esc(v)}</b></div>' for k, v in facts if v)
    tags = "".join(f'<span class="pill">{esc(t)}</span>' for t in csv(p.get("tags", "")))
    status = f'<span class="pill status"><i></i>{esc(p["status"])}</span>' if p.get("status") else ""

    shots = pairs(p["sections"].get("screens", ""))
    gallery = ""
    if shots:
        tiles = "".join(
            f'<button class="tile" data-src="../{esc(src)}" data-cap="{esc(cap)}">'
            f'<img src="../{esc(src)}" alt="{esc(cap or p["title"])}" loading="lazy">'
            f'{f"<span>{esc(cap)}</span>" if cap else ""}</button>'
            for src, cap in shots
        )
        gallery = f'<section class="gallery"><div class="tiles">{tiles}</div></section>'

    rows = ""
    for key, label in STORY:
        text = p["sections"].get(key, "")
        if text.strip():
            dark = " dark" if key == "outcome" else ""
            rows += f'<section class="row{dark}"><span class="pill">{label}</span><div class="txt">{rich(text)}</div></section>'
    story = f'<div class="story">{rows}</div>' if rows else ""

    metrics = pairs(p["sections"].get("metrics", ""))
    cstats = (
        '<div class="cstats">'
        + "".join(
            f'<div class="stat{" dark" if i == 0 else ""}"><small>{esc(l)}</small><b>{esc(v)}</b></div>'
            for i, (v, l) in enumerate(metrics)
        )
        + "</div>"
        if metrics
        else ""
    )

    idx = projects.index(p)
    nxt = projects[idx + 1] if idx + 1 < len(projects) else None
    if nxt:
        nxt_html = (
            f'<div><small>Next project</small><h3>{esc(nxt["title"])}</h3></div>'
            f'<a class="more" href="{esc(nxt.get("id", ""))}.html">Read case study <span>→</span></a>'
        )
    else:
        nxt_html = '<div><small>That is all for now</small><h3>Back to all work</h3></div><a class="more" href="../portfolio.html">Portfolio <span>→</span></a>'

    title = f"{p['title']} · {company} case study" if company else p["title"]
    sub = f'<p class="sub">{inline(p["summary"])}</p>' if p.get("summary") else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>{FONTS}
<style>{CSS}{CASE_CSS}</style></head><body><div class="wrap">
<nav class="nav"><a class="pill" href="../portfolio.html">← Portfolio</a><span class="pill">Case study</span></nav>
<header class="c-hero"><div class="meta">{status}{tags}</div><h1>{esc(p['title'])}</h1>{sub}</header>
<div class="facts">{facts_html}</div>
{gallery}{story}{cstats}
<section class="next">{nxt_html}</section>
<footer><span>{esc(profile.get('title', ''))}</span><span>Updated {esc(profile.get('updated', ''))}</span></footer>
</div><div class="lb" id="lb"><img alt=""></div><script>{CASE_JS}</script></body></html>"""


def build(profile, projects):
    projects = ordered(projects)
    screens = sum(len(pairs(p["sections"].get("screens", ""))) for p in projects)
    live = sum(1 for p in projects if p.get("status", "").lower() == "live")
    tools = {t for p in projects for t in csv(p.get("tools", ""))}
    role = profile.get("role", "Product Designer")
    company = profile.get("company", "")
    name = profile.get("name", "")
    stats = [
        (len(projects), "Projects", True),
        (screens, "Screens & assets", False),
        (live, "Live in production", False),
        (len(tools), "Tools used", False),
    ]
    stat_html = "".join(
        f'<div class="stat{" dark" if dark else ""}"><small>{esc(label)}</small><b>{n}</b></div>'
        for n, label, dark in stats
    )
    cards = "".join(project_html(p, i) for i, p in enumerate(projects))
    who = f"{esc(name)} · " if name else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(profile.get('title', 'Portfolio'))}</title>
{FONTS}
<style>{CSS}</style></head><body><div class="wrap">
<header class="hero"><div><span class="pill">{who}{esc(role)}{' · ' + esc(company) if company else ''}</span>
<h1>{esc(role)}{' at ' + esc(company) if company else ''}.<br><span>{esc(profile.get('tagline', ''))}</span></h1></div>
<p>Selected work, ordered by importance. Newest and highest-impact projects come first.</p></header>
<section class="stats">{stat_html}</section>
<div class="section-head"><h2>What I've built</h2><span class="pill">Case studies</span></div>
<main class="cases">{cards}</main>
<footer><span>Source: PORTFOLIO.md</span><span>Updated {esc(profile.get('updated', ''))}</span></footer>
</div><script>{JS}</script></body></html>"""


def main():
    profile, projects = parse(SRC.read_text(encoding="utf-8"))
    order = [PRIORITIES.index(p["priority"]) for p in projects if p.get("priority") in PRIORITIES]
    if order != sorted(order):
        print("warning: PORTFOLIO.md is not ordered P1 -> P3; the page is sorted, the file should be too", file=sys.stderr)
    for p in projects:
        for src, _ in pairs(p["sections"].get("screens", "")):
            if not (ROOT / src).exists():
                print(f"warning: missing file {src} in '{p['title']}'", file=sys.stderr)
    projects = ordered(projects)
    OUT.write_text(build(profile, projects), encoding="utf-8")
    CASES.mkdir(exist_ok=True)
    for stale in CASES.glob("*.html"):
        stale.unlink()
    for p in projects:
        if not p.get("id"):
            print(f"warning: '{p['title']}' has no id, so no case study page was built", file=sys.stderr)
            continue
        (CASES / f"{p['id']}.html").write_text(case_page(profile, p, projects), encoding="utf-8")
    print(f"built {OUT.name} and {len(projects)} case study page(s)")


if __name__ == "__main__":
    main()
