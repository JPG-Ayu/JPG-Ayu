#!/usr/bin/env python3
"""Generate self-hosted GitHub stat and repository SVG cards."""
from __future__ import annotations
import argparse,json,os,urllib.request,html
from pathlib import Path
THEMES={"dark":{"bg":"#0d1117","border":"#30363d","title":"#39d353","text":"#c9d1d9","muted":"#8b949e","value":"#e6edf3"},
"light":{"bg":"#fff","border":"#d0d7de","title":"#1a7f37","text":"#1f2328","muted":"#57606a","value":"#1f2328"}}
def api(path):
    r=urllib.request.Request("https://api.github.com"+path,headers={"User-Agent":"cards.py"})
    return json.loads(urllib.request.urlopen(r,timeout=30).read())
def esc(s): return html.escape(str(s),quote=True)
def frame(w,h,c,body,label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}"><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="10" fill="{c["bg"]}" stroke="{c["border"]}"/>{body}</svg>'
def stats(user,theme,out):
    c=THEMES[theme]; u=api(f"/users/{user}"); repos=api(f"/users/{user}/repos?per_page=100&type=owner")
    owned=[r for r in repos if not r.get("fork")]; stars=sum(r.get("stargazers_count",0) for r in owned)
    vals=[("Public repos",u.get("public_repos",0)),("Followers",u.get("followers",0)),("Following",u.get("following",0)),("Total stars",stars)]
    body=[f'<text x="22" y="36" font-size="15" font-weight="700" fill="{c["title"]}">{esc(user)}</text>']
    for i,(lab,val) in enumerate(vals):
        x=22+(i%2)*220; y=82+(i//2)*48
        body += [f'<text x="{x}" y="{y}" font-size="23" font-weight="700" fill="{c["value"]}">{esc(val)}</text>',
                 f'<text x="{x}" y="{y+17}" font-size="10.5" fill="{c["muted"]}">{esc(lab)}</text>']
    Path(out/f"card-stats-{theme}.svg").write_text(frame(480,170,c,"".join(body),f"{user} GitHub statistics"),encoding="utf-8")
    wanted=json.loads(Path("assets/projects.json").read_text())["projects"]
    by={r["name"].lower():r for r in repos}
    for e in wanted:
        r=by.get(e["repo"].lower())
        if not r: continue
        for t in THEMES:
            cc=THEMES[t]; desc=e.get("description") or r.get("description") or "No description yet."
            b=f'<text x="18" y="31" font-size="15" font-weight="700" fill="{cc["title"]}">{esc(r["name"])}</text>'
            b+=f'<text x="18" y="58" font-size="11.5" fill="{cc["text"]}">{esc(desc[:70])}</text>'
            b+=f'<text x="18" y="105" font-size="11" fill="{cc["muted"]}">{esc(e.get("language") or r.get("language") or "Unknown")} · ★ {r.get("stargazers_count",0)} · forks {r.get("forks_count",0)}</text>'
            Path(out/f"card-{r['name']}-{t}.svg").write_text(frame(420,132,cc,b,f'{r["name"]} repository card'),encoding="utf-8")
def main():
    p=argparse.ArgumentParser(); p.add_argument("--user",required=True); p.add_argument("--projects",default="assets/projects.json"); p.add_argument("--out",default="assets"); a=p.parse_args()
    out=Path(a.out); out.mkdir(exist_ok=True); stats(a.user,"dark",out); stats(a.user,"light",out)
if __name__=="__main__": main()
