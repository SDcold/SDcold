#!/usr/bin/env python3
"""Generates a self-contained animated terminal SVG for a GitHub profile README.
Only CSS animations inside the SVG document -> plays when embedded via <img>."""

W, H = 820, 478
PAD_X, TOP_BAR = 26, 36
CHAR_W, FONT = 9.0, 15          # monospace advance @15px ~= 9.0px
LINE_H, FIRST_Y = 26, 82
CPS = 16.0                       # typing speed for command lines
OUT_T = 0.20                     # output lines print quasi-instantly
GAP_IN, GAP_BLK = 0.28, 0.55     # pauses (s)
HOLD = 4.0                       # pause at end of cycle

C = {
    "bg": "#0b0f14", "chrome": "#121a23", "border": "#1e2a36",
    "p": "#39d353", "c": "#79c0ff", "a": "#c9d1d9", "o": "#adbac7",
    "s": "#a5d6ff", "k": "#ffa657", "n": "#6e7c8c", "ac": "#f778ba",
    "cy": "#56d4dd", "dim": "#7d8590",
}

# kind: cmd | out | blank ; segs: (text, colorkey)
LINES = [
    ("cmd", [("$ ", "p"), ("whoami", "c")]),
    ("out", [("KengneTalo", "cy"), (" // Full-Stack Engineer", "o")]),
    ("blank", []),
    ("cmd", [("$ ", "p"), ("cat ", "c"), ("stack.json", "a")]),
    ("out", [("{ ", "n"), ('"web"', "k"), (": [", "n"), ('"React"', "s"), (", ", "n"),
             ('"TypeScript"', "s"), (", ", "n"), ('"Next.js"', "s"), ("],", "n")]),
    ("out", [("  ", "n"), ('"api"', "k"), (": [", "n"), ('"Python"', "s"), (", ", "n"),
             ('"Django"', "s"), (", ", "n"), ('"Node.js"', "s"), ("],", "n")]),
    ("out", [("  ", "n"), ('"app"', "k"), (": [", "n"), ('"Qt/QML"', "s"), (", ", "n"),
             ('"Linux"', "s"), (", ", "n"), ('"Hyprland"', "s"), ("] }", "n")]),
    ("blank", []),
    ("cmd", [("$ ", "p"), ("ls ", "c"), ("~/projects", "a")]),
    ("out", [("wanzo/   fullup-hs/   nayee/   ats/", "o")]),
    ("blank", []),
    ("cmd", [("$ ", "p"), ("./now.sh", "c")]),
    ("out", [("> ", "ac"), ("Building from Cameroon, shipping across Africa", "o")]),
    ("blank", []),
]

# ---- timeline -------------------------------------------------------------
t, sched, prev = 0.6, [], None
for kind, segs in LINES:
    if kind == "blank":
        sched.append(None); prev = kind; continue
    n = sum(len(x) for x, _ in segs)
    dur = n / CPS if kind == "cmd" else OUT_T
    if prev is not None:
        t += GAP_BLK if (prev == "out" and kind == "cmd") else GAP_IN
    sched.append((t, t + dur, n))
    t += dur; prev = kind
END = t
CYCLE = round(END + HOLD, 2)
pc = lambda sec: round(sec / CYCLE * 100, 3)

# ---- build ----------------------------------------------------------------
css, body = [], []
for i, ((kind, segs), sc) in enumerate(zip(LINES, sched)):
    if sc is None:
        continue
    s, e, n = sc
    y = FIRST_Y + i * LINE_H
    x = PAD_X + 14
    width = n * CHAR_W + 6

    tspans = "".join(
        '<tspan fill="%s" xml:space="preserve">%s</tspan>' % (
            C[k], txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        for txt, k in segs)
    body.append(f'<text x="{x}" y="{y}" class="t">{tspans}</text>')
    body.append(
        f'<g class="w" style="animation-name:w{i};animation-timing-function:steps({n})">'
        f'<rect x="{x}" y="{y - 16}" width="{width}" height="{LINE_H - 4}" fill="{C["bg"]}"/>'
        f'<rect class="cur" x="{x}" y="{y - 14}" width="8.5" height="18" fill="{C["p"]}"'
        f' style="animation-name:c{i}"/></g>')

    css.append(f"@keyframes w{i}{{0%,{pc(s)}%{{transform:translateX(0)}}"
               f"{pc(e)}%,100%{{transform:translateX({round(width,1)}px)}}}}")
    css.append(f"@keyframes c{i}{{0%,{pc(s)}%{{opacity:0}}{pc(s)+.05}%,{pc(e)}%{{opacity:1}}"
               f"{pc(e)+.05}%,100%{{opacity:0}}}}")

# final blinking prompt
fy = FIRST_Y + len(LINES) * LINE_H
blink = [f"0%,{pc(END)}%{{opacity:0}}"]
tt, on = END, True
while tt < CYCLE - 0.05:
    blink.append(f"{pc(tt)+.05}%,{pc(min(tt+0.55, CYCLE))}%{{opacity:{1 if on else 0}}}")
    tt += 0.55; on = not on
css.append("@keyframes blink{" + "".join(blink) + "}")
body.append(f'<text x="{PAD_X + 14}" y="{fy}" class="t" fill="{C["p"]}">$</text>')
body.append(f'<rect class="bl" x="{PAD_X + 14 + 2 * CHAR_W}" y="{fy - 14}" width="8.5" '
            f'height="18" fill="{C["p"]}"/>')

SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Animated terminal: KengneTalo, Full-Stack Engineer">
<defs>
  <linearGradient id="glow" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{C['p']}" stop-opacity=".55"/>
    <stop offset=".5" stop-color="{C['cy']}" stop-opacity=".45"/>
    <stop offset="1" stop-color="{C['ac']}" stop-opacity=".5"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{C['cy']}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{C['cy']}" stop-opacity=".55"/>
    <stop offset="1" stop-color="{C['cy']}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="#1b2732"/>
  </pattern>
  <clipPath id="screen"><rect x="12" y="{12 + TOP_BAR}" width="{W - 24}" height="{H - 24 - TOP_BAR}"/></clipPath>
</defs>
<style>
  .t{{font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"DejaVu Sans Mono","Liberation Mono",monospace;font-size:{FONT}px;dominant-baseline:alphabetic}}
  .ttl{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12px;fill:{C['dim']}}}
  .w{{animation-duration:{CYCLE}s;animation-iteration-count:infinite;animation-fill-mode:both}}
  .cur{{animation-duration:{CYCLE}s;animation-iteration-count:infinite;animation-timing-function:linear}}
  {"".join(c for c in css if c)}
  .bl{{animation:blink {CYCLE}s steps(1) infinite}}
  .sweep{{animation:sweep 7s linear infinite}}
  @keyframes sweep{{0%{{transform:translateY(-40px)}}100%{{transform:translateY({H}px)}}}}
  .ring{{animation:ring 4s ease-in-out infinite}}
  @keyframes ring{{0%,100%{{opacity:.35}}50%{{opacity:.9}}}}
  @media (prefers-reduced-motion:reduce){{
    .w,.bl,.sweep,.ring{{animation:none}}
    .w{{transform:translateX(999px)}} .cur{{opacity:0}} .bl{{opacity:1}}
  }}
</style>

<rect width="{W}" height="{H}" rx="14" fill="{C['bg']}"/>
<rect class="ring" x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="url(#glow)" stroke-width="2"/>
<rect x="12" y="{12+TOP_BAR}" width="{W-24}" height="{H-24-TOP_BAR}" fill="url(#dots)"/>

<path d="M12 26a14 14 0 0 1 14-14h{W-52}a14 14 0 0 1 14 14v22H12z" fill="{C['chrome']}"/>
<line x1="12" y1="{12+TOP_BAR}" x2="{W-12}" y2="{12+TOP_BAR}" stroke="{C['border']}"/>
<circle cx="34" cy="30" r="6" fill="#ff5f57"/><circle cx="54" cy="30" r="6" fill="#febc2e"/><circle cx="74" cy="30" r="6" fill="#28c840"/>
<text x="{W/2}" y="34" class="ttl" text-anchor="middle">kengnetalo@github — ~/portfolio</text>

<g clip-path="url(#screen)">
  {chr(10).join("  " + b for b in body)}
  <rect class="sweep" x="12" y="0" width="{W-24}" height="34" fill="url(#scan)" opacity=".14"/>
</g>
</svg>'''

import sys, pathlib
out = pathlib.Path(sys.argv[1]); out.write_text(SVG, encoding="utf-8")
print(f"wrote {out}  cycle={CYCLE}s  typing_end={round(END,2)}s  {len(SVG)} bytes")
