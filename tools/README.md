# tools

The animated SVGs in `../assets/` are generated — edit the scripts, not the SVGs.

```sh
python3 tools/gen_header.py assets/header.svg   # terminal window
python3 tools/gen_footer.py assets/footer.svg   # matrix rain band
```

`assets/divider.svg` is hand-written and small enough to edit directly.

## Editing the terminal content

Everything lives in the `LINES` list in `gen_header.py`. Each entry is
`(kind, segments)` where `kind` is `cmd` (typed character by character),
`out` (printed at once) or `blank`, and each segment is `(text, color_key)`
with colors defined in the `C` dict. Timings, canvas size and typing speed
are the constants at the top — the animation timeline is recomputed on
every run, so lines can be added or removed freely.

## Previewing a specific frame

Browsers don't advance an SVG's animation clock on demand, so pause it and
seek with a negative delay:

```sh
sed "s|</style>|.w,.cur,.bl{animation-play-state:paused !important;animation-delay:-4.2s !important}\n</style>|" \
    assets/header.svg > /tmp/frame.svg
```

Then wrap `/tmp/frame.svg` in an HTML file and screenshot it headlessly.
