# controlflow-midi.github.io

Public site for **Control Flow**, a MIDI controller for iPhone and iPad.

Live at <https://controlflow-midi.github.io>.

## What's here

| Path | What it is |
|---|---|
| `index.html` | The whole site. Static, self-contained, no build step. |
| `maps/djay-pro/` | Downloadable djay Pro mapping files. |

## The MIDI reference table

`index.html` contains a table of every CC and note Control Flow sends. **Those
numbers are generated, not hand-written.** They come from the `SharedMIDI`
ledger in the app's `PlatformProfile.swift`, computed with the same
`base + item*itemStride + deck*deckStride` formula the app uses at runtime.

If the ledger changes in the app, regenerate this page rather than editing the
table by hand — a hand-edit is exactly how a published table silently stops
matching what the app actually sends.

## Deploying

GitHub Pages, served from the default branch root. Push to publish.

Adding a custom domain later: set it in Settings → Pages and commit a `CNAME`
file. GitHub then redirects `controlflow-midi.github.io` to the new domain
automatically, so links already shipped inside the app keep working.
