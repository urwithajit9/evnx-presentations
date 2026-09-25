# Audience decks — one per persona

Seven Beamer decks, each aimed at a specific room. They are **not** slices of
one deck: the same command lands differently depending on what the audience
ships, so each deck picks its own demos, its own honest limits, and its own
roadmap ordering.

| File | Room | Persona | Headline demo |
|---|---|---|---|
| [`frontend.tex`](frontend.tex) | Vite/React, Next.js, Vercel | RKS | `scan dist/` reports 0 files while a live key sits in the bundle |
| [`python-backend.tex`](python-backend.tex) | Django, FastAPI, Celery | AKS | `validate` on a real Django `.env` — 5 errors, 3 warnings |
| [`fullstack-java.tex`](fullstack-java.tex) | Spring Boot + Vue + React monorepo | RRP | `--prefix` generating three names from one base |
| [`ai-ml.tex`](ai-ml.tex) | Python, Jupyter, GPU boxes | SM | two OpenAI keys, one file, one detected |
| [`devops.tex`](devops.tex) | GitHub Actions, K8s, Terraform | NK | the exit contract and SARIF fingerprints |
| [`php-agency.tex`](php-agency.tex) | Laravel/Symfony agency | PT | `APP_DEBUG=true` in production passes clean |
| [`mobile.tex`](mobile.tex) | Expo, Flutter, EAS | MK | `--exclude "*_SECRET*"` letting the keystore password through |

Source personas: [`evnx-ecosystem-findings/04-user-stories/personas/`](../../evnx-ecosystem-findings/04-user-stories/personas/).

## Build

```bash
cd personas && pdflatex -interaction=nonstopmode frontend.tex && pdflatex -interaction=nonstopmode frontend.tex
```

Twice, for the table of contents. Each deck is standalone — it pulls
`persona-preamble.tex`, which pulls `../common/evnx-preamble.tex`.

There is no LaTeX toolchain on this machine, so the decks are **structurally
validated, not compiled**. `python3 ../check-tex.py` checks environment
balance, capture targets, `capturepart` ranges, `[fragile]` frames and `\input`
resolution across all 44 `.tex` files in the repo.

## Captures

Terminal blocks come from [`../captures/persona/`](../captures/persona) — 47
runs recorded against **evnx 0.5.2** for these decks. The root
[`../captures/`](../captures) pool (101 files, pinned to v0.5.0) is also
reachable, since `\capturedir` is `../captures` for both.

Nothing in these decks is transcribed or reconstructed. Where evnx misses
something, the miss is the capture.

## Four corrections to the source material

The persona files were written against the v0.5.0 README and release notes.
Re-running them against the binary moved four verdicts. Each correction is a
slide in the decks that it affects, not a footnote.

| Claim in the persona files | What the binary does | Decks affected |
|---|---|---|
| `evnx scan dist/` catches secrets inlined into bundles | `dist/` and `build/` are on the default exclusion list → **"0 files scanned", exit 0** | frontend, fullstack, mobile, devops |
| `scan notebooks/` detects keys in `.ipynb` JSON | `.ipynb` is not in the scannable-extension allowlist — **not scanned at all** | ai-ml |
| Multi-line values (PEM, JSON) are not supported | **They are.** Only double-quoted values containing escaped `\"` fail | python-backend, fullstack, ai-ml |
| `validate` warns about localhost in production | The rule is `check_localhost_docker` — gated on **Docker config**, not on environment | python-backend |

## Three findings that are new to this round

Not in any prior review, found while building these decks:

1. **The OpenAI detector matches the legacy key format only.** `sk-[0-9a-zA-Z]{48}`
   at `src/utils/patterns.rs:106` cannot match a modern `sk-proj-` project key,
   because of the hyphen. Those fall through to generic entropy at **low**
   severity, so `scan --severity high` reports a clean pass.
2. **`validate` has no model of framework load order.** A Symfony project where
   `.env` holds defaults and `.env.local` overrides is reported as missing
   variables — a false positive against how Symfony actually resolves config.
3. **`--exclude` is a denylist, and the documented mobile recipe leaks through it.**
   `convert --to json --exclude "*_SECRET*"` passes `ANDROID_KEYSTORE_PASSWORD`
   into the file that gets compiled into the app.

All three are written up in
[`../../evnx-devrel-review/tasks/persona-round-findings.md`](../../evnx-devrel-review/tasks/persona-round-findings.md).

## Presenting

[`AUDIENCE_PLAYBOOK.md`](AUDIENCE_PLAYBOOK.md) is the presenter's guide: the
opening line per room, which demo to lead with, the objection you will get, and
the honest answer to it. Read it before the deck.
