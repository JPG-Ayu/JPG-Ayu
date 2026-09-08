#!/usr/bin/env python3
"""Turn a photo into a green GitHub-style dot-matrix portrait."""
from __future__ import annotations
import argparse,math
from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance

def main():
    p=argparse.ArgumentParser()
    p.add_argument("image"); p.add_argument("-o","--out",required=True); p.add_argument("--cols",type=int,default=88)
    p.add_argument("--circle",action="store_true"); p.add_argument("--color",action="store_true")
    p.add_argument("--equalize",action="store_true"); p.add_argument("--detail",type=float,default=0.0)
    p.add_argument("--mode",default="dots"); a=p.parse_args()
    img=ImageOps.exif_transpose(Image.open(a.image)).convert("RGB")
    if a.equalize: img=ImageOps.equalize(img)
    if a.detail: img=ImageEnhance.Contrast(img).enhance(1+a.detail)
    w,h=img.size; rows=max(1,round(a.cols*h/w*0.5)); small=img.resize((a.cols,rows))
    gray=ImageOps.grayscale(small); px=gray.load(); rgb=small.load()
    fg="#39d353"; light="#216e39"
    def svg(theme):
        fgx=fg if theme=="dark" else light
        out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {a.cols*8+8} {rows*8+8}" width="{a.cols*8+8}" height="{rows*8+8}">']
        for y in range(rows):
            for x in range(a.cols):
                if a.circle:
                    nx=(x+.5)/a.cols*2-1; ny=(y+.5)/rows*2-1
                    if math.hypot(nx,ny)>1.0: continue
                v=px[x,y]/255; r=1.0+v*2.8; op=.12+v*.88
                color=(f"#{rgb[x,y][0]:02x}{rgb[x,y][1]:02x}{rgb[x,y][2]:02x}" if a.color else fgx)
                out.append(f'<circle cx="{x*8+4}" cy="{y*8+4}" r="{r:.2f}" fill="{color}" opacity="{op:.2f}"/>')
        out.append("</svg>"); return "".join(out)
    Path(a.out+"-dark.svg").write_text(svg("dark"),encoding="utf-8")
    Path(a.out+"-light.svg").write_text(svg("light"),encoding="utf-8")
if __name__=="__main__": main()
