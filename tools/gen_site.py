#!/usr/bin/env python3
"""Generate index.html for controlflow-midi.github.io.

Addresses are computed with the same formula as MIDIAllocation.address() in
PlatformProfile.swift (base + item*itemStride + deck*deckStride) so the
published table cannot drift from the ledger by transcription error.
"""

import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")

# (name, kind, base, itemStride, itemCount, deckStride, deckCount)
# mirrored from SharedMIDI in PlatformProfile.swift
LEDGER = {
    "fx-wetdry":       ("cc",   20, 2, 3, 6, 2),
    "fx-opp":          ("cc",   21, 2, 3, 6, 2),
    "fx-onoff":        ("note", 30, 1, 3, 3, 2),
    "fx-ceiling":      ("note", 83, 1, 3, 3, 2),
    "fx-ceilinglong":  ("note", 36, 1, 3, 3, 2),
    "fx-floor":        ("note", 89, 1, 3, 3, 2),
    "fx-floorlong":    ("note", 42, 1, 3, 3, 2),
    "fx-prev":         ("note", 23, 1, 3, 3, 2),
    "fx-next":         ("note", 48, 1, 3, 3, 2),
    "stems-volume":    ("cc",   40, 1, 4, 8, 2),
    "stems-fxsend":    ("cc",   44, 1, 4, 8, 2),
    "stems-solo":      ("note", 95, 1, 4, 4, 2),
    "stems-mute":      ("note", 103, 1, 4, 4, 2),
    "stems-mutelong":  ("note", 56, 1, 4, 4, 2),
    "stems-fxenable":  ("note", 111, 1, 4, 4, 2),
    "xy-x":            ("cc",   56, 2, 3, 6, 2),
    "xy-y":            ("cc",   57, 2, 3, 6, 2),
    "xy-button":       ("note", 15, 1, 4, 4, 2),
    "pads-note":       ("note", 64, 1, 8, 8, 2),
}

# display label, and whether the numbers are confirmed against a real host
LABELS = {
    "fx-wetdry":      "Parameter A (wet/dry)",
    "fx-opp":         "Parameter B",
    "fx-onoff":       "Slot on/off",
    "fx-ceiling":     "Top button — tap",
    "fx-ceilinglong": "Top button — long press",
    "fx-floor":       "Bottom button — tap",
    "fx-floorlong":   "Bottom button — long press",
    "fx-prev":        "Previous effect",
    "fx-next":        "Next effect",
    "stems-volume":   "Stem volume",
    "stems-fxsend":   "Stem FX send",
    "stems-solo":     "Stem solo",
    "stems-mute":     "Stem mute — tap",
    "stems-mutelong": "Stem mute — long press",
    "stems-fxenable": "Stem FX enable",
    "xy-x":           "X axis",
    "xy-y":           "Y axis",
    "xy-button":      "Trigger button",
    "pads-note":      "Pad trigger",
}

BLOCKS = [
    ("FX", "Three effect slots per deck.",
     ["fx-wetdry", "fx-opp", "fx-onoff", "fx-ceiling", "fx-ceilinglong",
      "fx-floor", "fx-floorlong", "fx-prev", "fx-next"]),
    ("Stems", "Four stems per deck.",
     ["stems-volume", "stems-fxsend", "stems-solo", "stems-mute",
      "stems-mutelong", "stems-fxenable"]),
    ("XY Pad", "Three slots per deck, plus four trigger buttons.",
     ["xy-x", "xy-y", "xy-button"]),
    ("Pads", "Eight pads per deck.", ["pads-note"]),
]

ITEM_WORD = {"fx": "Slot", "stems": "Stem", "xy": "Slot", "pads": "Pad"}


def addresses(name, deck):
    _kind, base, istride, icount, dstride, _dcount = LEDGER[name]
    return [base + i * istride + deck * dstride for i in range(icount)]


def fmt(addrs):
    """Contiguous runs collapse to a range; anything else lists out."""
    if len(addrs) > 2 and all(b - a == 1 for a, b in zip(addrs, addrs[1:])):
        return f"{addrs[0]}&ndash;{addrs[-1]}"
    return ", ".join(str(a) for a in addrs)


def rows_for(names):
    out = []
    for name in names:
        kind = LEDGER[name][0]
        item_word = ITEM_WORD[name.split("-")[0]]
        count = LEDGER[name][3]
        out.append(
            f"      <tr>\n"
            f"        <td>{LABELS[name]}<br><code>{name}</code></td>\n"
            f'        <td class="kind">{kind.upper()}</td>\n'
            f'        <td class="num">{fmt(addresses(name, 0))}</td>\n'
            f'        <td class="num">{fmt(addresses(name, 1))}</td>\n'
            f'        <td class="note">{item_word}s 1&ndash;{count}, ascending</td>\n'
            f"      </tr>"
        )
    return "\n".join(out)


def main():
    sections = []
    for title, blurb, names in BLOCKS:
        sections.append(f"""<section>
  <h3>{title}</h3>
  <p class="blurb">{blurb}</p>
  <div class="scroller">
    <table>
      <thead>
        <tr><th>Control</th><th>Type</th><th>Deck 1</th><th>Deck 2</th><th>Order</th></tr>
      </thead>
      <tbody>
{rows_for(names)}
      </tbody>
    </table>
  </div>
</section>""")

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Control Flow — MIDI Reference</title>
<meta name="description" content="MIDI reference and mappings for Control Flow, a MIDI controller for iPhone and iPad.">
<style>
  :root {{
    --bg: #fdf6e3; --fg: #073642; --muted: #657b83; --line: #e6dcc3;
    --card: #fffaf0; --accent: #268bd2;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #002b36; --fg: #eee8d5; --muted: #93a1a1; --line: #0c3f4c;
      --card: #073642; --accent: #2aa198;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 2.5rem 1.25rem 5rem;
    background: var(--bg); color: var(--fg);
    font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    -webkit-text-size-adjust: 100%;
  }}
  .wrap {{ max-width: 60rem; margin: 0 auto; }}
  h1 {{ font-size: 2rem; margin: 0 0 .25rem; letter-spacing: -.02em; }}
  .tagline {{ color: var(--muted); margin: 0 0 2.5rem; font-size: 1.05rem; }}
  h2 {{ font-size: 1.35rem; margin: 3rem 0 .5rem; padding-bottom: .4rem; border-bottom: 1px solid var(--line); }}
  h3 {{ font-size: 1.05rem; margin: 2rem 0 .25rem; }}
  p {{ margin: .5rem 0; }}
  .blurb {{ color: var(--muted); font-size: .9rem; margin: 0 0 .75rem; }}
  .scroller {{ overflow-x: auto; -webkit-overflow-scrolling: touch; }}
  table {{ border-collapse: collapse; width: 100%; font-size: .875rem; min-width: 34rem; }}
  th, td {{ text-align: left; padding: .55rem .7rem; border-bottom: 1px solid var(--line); vertical-align: top; }}
  th {{ font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); font-weight: 600; }}
  code {{ font: .8em ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--muted); }}
  .kind, .num {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; white-space: nowrap; }}
  .kind {{ color: var(--muted); font-size: .8rem; }}
  .note {{ color: var(--muted); font-size: .8rem; }}
  .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 1rem 1.25rem; margin: 1.25rem 0; }}
  .card p:first-child {{ margin-top: 0; }}
  .card p:last-child {{ margin-bottom: 0; }}
  ol, ul {{ padding-left: 1.25rem; }}
  li {{ margin: .3rem 0; }}
  footer {{ margin-top: 4rem; padding-top: 1.25rem; border-top: 1px solid var(--line); color: var(--muted); font-size: .85rem; }}
  a {{ color: var(--accent); }}
</style>
</head>
<body>
<div class="wrap">

  <h1>Control Flow</h1>
  <p class="tagline">A MIDI controller for iPhone and iPad. This page is the MIDI reference.</p>

  <div class="card">
    <p><strong>Control Flow sends standard MIDI over Bluetooth.</strong> It doesn't know or
    care what your host app does with a message — you decide that by MIDI-Learning each
    control in the host. This page lists every address the app sends, so you can map by
    hand or check what a control is bound to.</p>
  </div>

  <h2>How to map a control</h2>
  <ol>
    <li>Connect Control Flow to your host over Bluetooth MIDI.</li>
    <li>In the host, start MIDI Learn on the parameter you want to control.</li>
    <li>Move or tap the control in Control Flow.</li>
    <li>The host binds it. Repeat per control.</li>
  </ol>

  <h2>MIDI reference</h2>
  <p>Deck 1 sends on channel 1, deck 2 on channel 2. Every control also has its own
  unique CC or note number, so decks stay distinct even in hosts that ignore the channel
  entirely — <strong>djay Pro is one of them</strong>, and identifies controls by number alone.</p>
  <p>CC and note are independent 0&ndash;127 spaces, so a CC 30 and a note 30 are different
  addresses.</p>

{chr(10).join(sections)}

  <h2>Downloadable mappings</h2>

  <section>
    <h3>djay Pro</h3>
    <p class="blurb">A ready-made mapping, so you don't have to MIDI-Learn every control by hand.</p>
    <div class="card">
      <p><a href="maps/djay-pro/control-flow-djay-pro.djayMidiMapping" download><strong>Download the djay Pro mapping</strong></a></p>
      <!-- INSTALL-STEPS: replace with the real djay Pro import steps -->
      <ol>
        <li>Download the file above.</li>
        <li>Import it in djay Pro.</li>
        <li>Connect Control Flow over Bluetooth MIDI and select the mapping.</li>
      </ol>
      <p class="blurb">Anything the mapping doesn't cover, you can still MIDI-Learn
      yourself using the table above.</p>
    </div>
  </section>

  <footer>
    <p>Control Flow is an independent app. djay Pro, Serato, and Ableton Live are
    trademarks of their respective owners and are not affiliated with this project.</p>
  </footer>

</div>
</body>
</html>
"""
    with open(OUT, "w") as f:
        f.write(html)
    print(f"wrote {OUT} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
