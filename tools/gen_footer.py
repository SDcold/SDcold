#!/usr/bin/env python3
"""Animated 'matrix rain' footer band, self-contained CSS animations."""
import random, sys, pathlib

W, H, COL, CH = 820, 150, 15, 16
random.seed(7)
GLYPHS = "01ABCDEFGHJKLMNPQRSTUVWXYZ<>{}[]/\\$#*+=-_|~^&%!?abcdefghijkmnopqrstuvwxyz"

cols, css = [], []
for i, cx in enumerate(range(8, W - 6, COL)):
    n = random.randint(6, 14)
    dur = round(random.uniform(9.0, 20.0), 2)
    delay = round(random.uniform(-20.0, 0), 2)
    span = n * CH
    tspans = "".join(
        '<tspan x="%d" dy="%d" fill="%s" fill-opacity="%.2f">%s</tspan>'
        % (cx, CH, "#8fae9c" if j == n - 1 else "#566a60",
           0.10 + 0.40 * (j / max(n - 1, 1)) ** 2,
           random.choice(GLYPHS).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        for j in range(n))
    cols.append(f'<text class="r r{i}" x="{cx}" y="{-span}">{tspans}</text>')
    css.append(f".r{i}{{animation-duration:{dur}s;animation-delay:{delay}s}}")
    css.append(f"@keyframes f{i}{{0%{{transform:translateY(0)}}"
               f"100%{{transform:translateY({H + span}px)}}}}")
    css.append(f".r{i}{{animation-name:f{i}}}")

SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Thanks for scrolling">
<defs>
  <linearGradient id="vg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".35" stop-color="#fff" stop-opacity=".85"/>
    <stop offset=".72" stop-color="#fff" stop-opacity=".25"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#vg)"/></mask>
  <linearGradient id="plate" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#0f1318" stop-opacity="0"/>
    <stop offset=".22" stop-color="#0f1318" stop-opacity=".92"/>
    <stop offset=".78" stop-color="#0f1318" stop-opacity=".92"/>
    <stop offset="1" stop-color="#0f1318" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#0f1318"/><stop offset=".12" stop-color="#0f1318" stop-opacity="0"/>
    <stop offset=".88" stop-color="#0f1318" stop-opacity="0"/><stop offset="1" stop-color="#0f1318"/>
  </linearGradient>
</defs>
<style>
  .r{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"DejaVu Sans Mono",monospace;font-size:13px;animation-timing-function:linear;animation-iteration-count:infinite}}
  .cap{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:16px;fill:#aab3bd}}
  .hl{{fill:#8fae9c}}
  .cur2{{animation:bk 1.1s steps(1) infinite}}
  @keyframes bk{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
  {"".join(css)}
  @media (prefers-reduced-motion:reduce){{.r,.cur2{{animation:none}}.cur2{{opacity:1}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="#0f1318"/>
<g mask="url(#m)">{"".join(cols)}</g>
<rect width="{W}" height="{H}" rx="14" fill="url(#edge)"/>
<rect x="{W/2 - 340}" y="{H/2 - 20}" width="680" height="40" fill="url(#plate)"/>
<text x="{W/2}" y="{H/2 + 6}" class="cap" text-anchor="middle">&gt; <tspan class="hl">thanks for scrolling</tspan> — let&apos;s build something</text>
<rect class="cur2" x="{W/2 + 225}" y="{H/2 - 8}" width="9" height="17" fill="#8fae9c"/>
</svg>'''
pathlib.Path(sys.argv[1]).write_text(SVG, encoding="utf-8")
print(f"wrote footer  {len(cols)} columns  {len(SVG)} bytes")
