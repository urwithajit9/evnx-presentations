# evnx presentations — Beamer sources

Ten decks, built from **real execution output**. No output in these slides was
typed by hand; every terminal block is `\input` from a file in `captures/`.

**Three general decks**, captured from `evnx 0.5.0` at tag `v0.5.0` (`85a52c3`):

| Deck | Audience | Frames |
|---|---|---|
| [`user-guide/`](user-guide) | Users — every command, syntax, flags, use cases | 88 |
| [`use-cases/`](use-cases) | Developer advocacy — workflows combining commands + cloud sync | 26 |
| [`architecture/`](architecture) | Rust contributors — ecosystem, internals, testing, conventions | 26 |

**Seven audience decks** in [`personas/`](personas), captured from `evnx 0.5.2`.
One per stack, because the same command lands differently depending on what the
room ships:

| Deck | Room | Headline demo |
|---|---|---|
| [`frontend.tex`](personas/frontend.tex) | Vite/React, Next.js, Vercel | `scan dist/` reports 0 files over a live key |
| [`python-backend.tex`](personas/python-backend.tex) | Django, FastAPI, Celery | `validate` on a real Django `.env` |
| [`fullstack-java.tex`](personas/fullstack-java.tex) | Spring Boot + Vue + React monorepo | `--prefix` generating three names from one base |
| [`ai-ml.tex`](personas/ai-ml.tex) | Python, Jupyter, GPU boxes | two OpenAI keys, one file, one detected |
| [`devops.tex`](personas/devops.tex) | GitHub Actions, K8s, Terraform | the exit contract and SARIF fingerprints |
| [`php-agency.tex`](personas/php-agency.tex) | Laravel/Symfony agency | `APP_DEBUG=true` in production passes clean |
| [`mobile.tex`](personas/mobile.tex) | Expo, Flutter, EAS | `--exclude` letting the keystore password through |

[`personas/AUDIENCE_PLAYBOOK.md`](personas/AUDIENCE_PLAYBOOK.md) is the
presenter's guide — opening line, lead demo, the objection you will get, and the
answer. Read it before the deck.

---

## ⚠️ Not compile-verified

**There is no LaTeX toolchain on the machine these were written on**
(`pdflatex` absent; installing texlive needs an interactive `sudo`). The sources
are therefore **structurally validated but not compiled**. Run
`python3 check-tex.py` and then build — expect to fix minor typesetting nits on
the first real run (overfull boxes, a frame that wants `\small`).

What `check-tex.py` does verify, on all 36 `.tex` files:

- `\begin{…}` / `\end{…}` balance, with the offending line number
- every `\capture{f}` and `\capturepart{f}{a}{b}` target exists
- `\capturepart` line ranges are inside the file
- every frame containing verbatim content is marked `[fragile]`
- every `\input{…}` target resolves

```bash
python3 check-tex.py
# checked 36 .tex files, 156 frames, 62 capture references
# RESULT: PASS — no structural errors
```

---

## Building

```bash
sudo apt-get install -y \
  texlive-latex-recommended texlive-latex-extra \
  texlive-fonts-recommended texlive-pictures
```

`texlive-pictures` is needed for TikZ (the ecosystem diagram in
`architecture/`). `texlive-latex-extra` supplies `beamer`.

```bash
cd user-guide    && pdflatex -interaction=nonstopmode main.tex && pdflatex main.tex
cd ../use-cases  && pdflatex -interaction=nonstopmode main.tex && pdflatex main.tex
cd ../architecture && pdflatex -interaction=nonstopmode main.tex && pdflatex main.tex
```

Run twice — the second pass resolves `\tableofcontents`.

`latexmk -pdf main.tex` does both passes if you have it.

---

## Layout

```
evnx-presentations/
├── check-tex.py              structural validator (no LaTeX needed)
├── common/
│   └── evnx-preamble.tex     theme, colours, listings style, glyph mapping
├── captures/                 101 real runs from v0.5.0
│   └── persona/              47 more, recorded against 0.5.2
├── user-guide/
│   ├── main.tex              the combined deck
│   ├── commands/cmd-*.tex    16 files, frames only, no preamble
│   └── standalone/*.tex      16 one-command decks that build alone
├── use-cases/main.tex
├── architecture/main.tex
└── personas/
    ├── persona-preamble.tex  shared by the seven audience decks
    ├── AUDIENCE_PLAYBOOK.md  how to present to each room
    └── <audience>.tex        7 standalone decks
```

### Per-command decks

Each command's frames live in **one file with no preamble**, so they can be
used two ways:

```bash
# all 16 commands, one deck
cd user-guide && pdflatex main.tex

# just evnx scan
cd user-guide/standalone && pdflatex scan.tex
```

Adding a command means writing `commands/cmd-foo.tex`, adding one
`\input{commands/cmd-foo}` line to `main.tex`, and dropping a wrapper in
`standalone/`.

---

## The capture mechanism

Slides never contain pasted output. They reference it:

```latex
\capture{24-scan.txt}                  % the whole run
\capturepart{28-scan-sarif.txt}{1}{20} % lines 1–20
```

Each capture file starts with the command that produced it and ends with its
exit code:

```
$ evnx validate --no-color
  ...
[exit 1]
```

**To refresh after a code change**, re-run the capture commands against a new
build and the slides update with no LaTeX edits. The validator will tell you if
a `\capturepart` range no longer fits.

### Unicode

evnx emits exactly 11 non-ASCII characters — enumerated from the captures, not
guessed: `─ — · ✓ → ✗ … ⚠ U+FE0F • ↔`. The preamble maps each one twice:
`newunicodechar` for body text, and a `literate` rule for `listings`
(`newunicodechar` does not apply inside verbatim). This is why the decks build
under plain **pdfLaTeX** without a Unicode font.

---

## Accuracy

Everything factual was executed before it was written. Where a claim could not
be verified it was cut, and several first drafts were corrected during writing:

- `evnx doctor` was said to flag `localhost` under Docker — **it does not**;
  that check belongs to `validate` and only fires when Docker config is present.
- `evnx init` was described as run-once — it has a `--force` flag and refuses
  with exit `2` otherwise.
- `backup --password-file` and `restore --key-file` are accepted but **not**
  shown in `--help`; the slide says so rather than implying the help is complete.
- Shell-completion line counts were re-measured at this commit (3,432 / 2,771 /
  551 / 1,376).
- `backup --verify` exists and is covered.

**Scope note on the cloud family.** The machine these were captured on holds
live credentials, so `auth`, `vault` and `cloud` captures are help output,
offline behaviour and the transport guard only. Nothing was pushed, shared or
revoked against `api.evnx.dev`, and the one account address that appeared was
redacted to `you@example.com`.

**Version.** The decks are pinned to the released tag **`v0.5.0` = `85a52c3`**, not
to a moving branch. Every capture was regenerated from a binary built at that tag
and verified byte-identical (18 `--help` captures, 0 differences).

To re-pin for a future release: update `\verifiedon` in
`common/evnx-preamble.tex`, the title-slide line in each `main.tex`, the
`standalone/*.tex` subtitle line, and `captures/00-baseline.txt`.
