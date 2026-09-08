#!/usr/bin/env python3
"""Render a GitHub-style radar chart as dark/light SVGs."""
from __future__ import annotations
import argparse, json, math, os, urllib.request
from pathlib import Path

THEMES = {
    "dark": {"grid":"#30363d","spoke":"#21262d","label":"#c9d1d9","value":"#8b949e","title":"#e6edf3","fill":"#39d353","stroke":"#3fb950"},
    "light":{"grid":"#d0d7de","spoke":"#e6eaef","label":"#1f2328","value":"#57606a","title":"#1f2328","fill":"#2da44e","stroke":"#1a7f37"},
}
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
def github_languages(user, limit=7):
    req = urllib.request.Request(f"https://api.github.com/users/{user}/repos?per_page=100&type=owner&sort=pushed",
                                 headers={"User-Agent":"radar.py"})
    repos = json.loads(urllib.request.urlopen(req, timeout=30).read())
    totals={}
    for repo in repos:
        if repo.get("fork") or repo.get("archived"): continue
        try:
            r=urllib.request.Request(repo["languages_url"],headers={"User-Agent":"radar.py"})
            langs=json.loads(urllib.request.urlopen(r,timeout=30).read())
        except Exception: continue
        for k,v in langs.items(): totals[k]=totals.get(k,0)+v
    top=sorted(totals.items(),key=lambda x:-x[1])[:limit]
    if not top: return f"{user} · language mix",[("No public code",50)]
    peak=top[0][1]
    return f"{user} · language mix",[(k,round(100*(v/peak)**0.5,1)) for k,v in top]

def render(title, axes, theme, out):
    c=THEMES[theme]; n=len(axes); size=360; cx=180; cy=190; r=125
    pts=lambda rr:[(cx+rr*math.cos(-math.pi/2+i*2*math.pi/n),
                    cy+rr*math.sin(-math.pi/2+i*2*math.pi/n)) for i in range(n)]
    outer=pts(r)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} 390" width="{size}" height="390" font-family="ui-sans-serif,Arial">']
    parts.append(f'<text x="{cx}" y="24" text-anchor="middle" font-size="16" font-weight="700" fill="{c["title"]}">{esc(title)}</text>')
    for level in range(20,101,20):
        p=pts(r*level/100); parts.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in p)}" fill="none" stroke="{c["grid"]}" stroke-width="1"/>')
    for i,(x,y) in enumerate(outer):
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{c["spoke"]}"/>')
        lx=cx+(r+24)*math.cos(-math.pi/2+i*2*math.pi/n); ly=cy+(r+24)*math.sin(-math.pi/2+i*2*math.pi/n)
        anchor="middle" if abs(lx-cx)<12 else ("start" if lx>cx else "end")
        parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="12" fill="{c["label"]}">{esc(x:=axes[i][0])}</text>')
        parts.append(f'<text x="{lx:.1f}" y="{ly+14:.1f}" text-anchor="{anchor}" font-size="10" fill="{c["value"]}">{axes[i][1]:g}</text>')
    val=pts_for=[(cx+r*max(0,min(100,v))/100*math.cos(-math.pi/2+i*2*math.pi/n),
                  cy+r*max(0,min(100,v))/100*math.sin(-math.pi/2+i*2*math.pi/n)) for i,(_,v) in enumerate(axes)]
    parts.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in val)}" fill="{c["fill"]}" fill-opacity=".18" stroke="{c["stroke"]}" stroke-width="2"/>')
    for x,y in val: parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{c["stroke"]}"/>')
    parts.append("</svg>")
    Path(f"{out}-{theme}.svg").write_text("".join(parts),encoding="utf-8")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--data"); p.add_argument("--github"); p.add_argument("-o","--out",required=True)
    a=p.parse_args()
    if a.github: title,axes=github_languages(a.github)
    else:
        d=json.loads(Path(a.data).read_text()); title=d.get("title","Skill Radar"); axes=[(x["label"],float(x["value"])) for x in d["axes"]]
    for t in THEMES: render(title,axes,t,a.out)
if __name__=="__main__": main()
