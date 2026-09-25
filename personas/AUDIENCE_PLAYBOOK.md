# Presenter's playbook

How to present evnx to a specific room. One section per audience: the opening,
the demo that lands, the objection you will get, and what to say back.

The rule underneath all of it: **lead with the limit that room will discover on
their own within a week.** Every one of these audiences will run the tool after
the talk. Whatever you hid, they find — and then nothing else you said counts.

---

## The universal shape

Whatever the room, the arc is the same:

1. **Their Monday** — describe a week they have actually had. No product yet.
2. **Which of those a file tool can even touch** — draw the boundary yourself,
   before they do.
3. **One command that fixes one of them, live.**
4. **One command that looks like it works and does not** — with the real output.
5. **The adoption path** — copy-paste, including the workarounds.
6. **The roadmap** — and invite them to argue about the order.

Step 4 is the one people skip. It is the one that earns the room.

### Three things to say once, in any deck

- **"evnx guards the file. Your framework guards the process."** This is the
  honest scope, and it heads off "why doesn't it catch X at runtime".
- **Exit `2` means *could not run*, and it is not a pass.** Every audience with
  a pipeline cares; nobody else's scanner does this well.
- **The server cannot read your secrets — passively.** Volunteer the
  key-substitution caveat. Credibility for the whole talk is bought here.

### Timing cuts

| Slot | Cut to |
|---|---|
| **5 min** (lightning) | Their Monday → the one failing demo → the roadmap slide |
| **20 min** (meetup) | Drop the crypto slide and one workflow section |
| **45 min** (workshop) | Everything, and have them run the adoption block on their own repo |

---

## Frontend — Vite, Next.js, Vercel

**Deck:** [`frontend.tex`](frontend.tex)

**Open with:** *"Who has shipped a secret key to the browser behind a
`NEXT_PUBLIC_` prefix?"* Hands go up, or people laugh, which is the same answer.

**Lead demo:** `evnx validate` on a `.env.local` holding a live Stripe key named
`NEXT_PUBLIC_STRIPE_KEY`. It passes clean, exit `0`. Then `evnx scan` on the
same file catches it. The point: **use `scan` as your prefix guard, not
`validate`** — and neither of them understands what the prefix means.

**Then the trap:** `evnx scan dist/` → "✓ No secrets detected", "0 files
scanned". The recommended workaround is broken. `.next/static/` works only
because that directory name is not on the exclusion list.

**Objection you will get:** *"So why would I use this instead of gitleaks?"*

**Answer:** You would use both. gitleaks scans history; evnx is the `.env`
lifecycle — sharing, drift, onboarding, validation — with scanning attached. If
all you want is history scanning, use gitleaks and skip this talk.

**Do not oversell:** `cloud run` removes the plaintext file, not the master
password, and your public vars still end up in the bundle by design.

---

## Python backend — Django, FastAPI, Celery

**Deck:** [`python-backend.tex`](python-backend.tex)

**Open with:** the `DEBUG="False"` incident. Django error pages with full
settings, publicly visible, because a non-empty string is truthy. This room has
all lived it.

**Lead demo:** `evnx validate --validate-formats` on a realistic Django `.env`.
Five errors, three warnings, every one of them a bug with a name. This is the
strongest single demo in any of the seven decks — the rules were written from
the same incident reports the room remembers.

**Then the correction:** multi-line PEM values work. The claim that they do not
has been repeated into a roadmap item. Run it live; it takes ten seconds. Then
show the one shape that breaks — double quotes containing escaped `\"` — and
give them the fix (single-quote JSON).

**Objection you will get:** *"pydantic already validates my settings."*

**Answer:** It validates the process, once the process boots, on your machine.
It cannot tell you your teammate's `.env` is missing a key, or that
`SECRET_KEY` is still a placeholder in the file that is about to be deployed.
Show the slide where the gaps are complementary — `PostgresDsn` catches the
scheme typo evnx lets through; `SecretStr` covers the logging gap evnx marks
unsolved. That slide converts people.

**Do not overstate:** there is no "localhost in production" rule. It is
`check_localhost_docker`, gated on Docker config. And warnings never fail the
command — `--strict` does not change that, it means "also report undeclared
variables".

---

## Full-stack Java — Spring Boot + Vue + React monorepo

**Deck:** [`fullstack-java.tex`](fullstack-java.tex)

**Open with:** the new laptop that will not start the backend because
`DB_PASSWORD` lives in a colleague's IntelliJ run configuration. Twelve
variables copied from a screenshot.

**Lead demo:** `evnx cloud run -- ./mvnw spring-boot:run`. No
`spring.config.import`, no EnvFile plugin, no code change — relaxed binding maps
`SPRING_DATASOURCE_URL` onto `spring.datasource.url` for free. This is a clean
win and it is the reason this room stays.

**Second demo:** `--prefix VITE_` and `--prefix REACT_APP_` side by side,
generating two names from one base value. It turns "I forgot to update the React
one" into a structural impossibility.

**Objection you will get:** *"We already have HashiCorp Vault."*

**Answer:** Then do not try to replace it. Decide the source of truth **per
environment**: evnx for local and dev, Vault for staging and production,
`convert`/`migrate` as the hand-off. Two systems both claiming to own production
is the actual failure mode — say that before they do.

**Be precise about:** `scan` reads `.yml`, `.java`, `.properties` and more — the
"it only reads `.env`" assumption is wrong and it is what makes the tool useful
on a Spring codebase. And there is **no** monorepo model: three directories
means three commands.

---

## AI / ML — Python, Jupyter, rented GPUs

**Deck:** [`ai-ml.tex`](ai-ml.tex)

**Open with:** the invoice. A leaked web key is an incident; a leaked LLM key is
an incident *and* a bill. This reframes secret hygiene as cost control, which
this audience has budget for.

**Lead demo:** `evnx cloud run -- python train.py`. No `.env` to `scp` to a GPU
box, nothing left behind on a machine you destroy at lunchtime, nothing on the
shared cluster filesystem. Highest-value change for this room and it works
today.

**Then the two misses, in order:**

1. `.ipynb` is not scanned. Show the notebook and its byte-identical `.json`
   copy — one finding, and it is the `.json`.
2. Two OpenAI keys in one file: the legacy `sk-` one is flagged **high**, the
   modern `sk-proj-` one falls to **low** entropy. `--severity high` reports a
   clean pass.

**Objection you will get:** *"Then why would I trust this scanner at all?"*

**Answer:** Because you would not trust any scanner as your only control. Then
recommend `nbstripout` — which is not an evnx feature, and is the right first
move regardless of what scanner you use. Recommending the competitor's answer is
what buys credibility for the rest.

**Also say:** `cloud run` still prompts for the master password on a shared GPU
box. Machine identities are not built. Do not let someone discover that on a
university cluster.

---

## DevOps / platform — GitHub Actions, K8s, Terraform

**Deck:** [`devops.tex`](devops.tex)

**Open with the recommendation, not the pitch:** adopt the CLI across every repo
as a CI gate; use evnx cloud for developer-local only; do not plan to replace
Secrets Manager this year. This room has been sold to before and respects being
told the boundary first.

**Lead demo:** the exit contract. `0` / `1` / `2`, with `2` meaning *could not
run* and printing "No verdict: evnx did not finish. This is not a clean result."
Most tools conflate "clean" with "did not run". Then SARIF with
`partialFingerprints` — the reason their code-scanning alerts stop resetting
every run.

**Then the trap, generalised:** a scanner's worst outcome is a confident pass.
Show `scan dist/` → "0 files scanned", exit `0`. Then give them the fix that
outlives the bug:

```bash
n=$(evnx scan "$TARGET" --format json | jq '.files_scanned')
test "$n" -gt 0 || { echo "scan covered no files"; exit 1; }
```

Assert the denominator in **every** coverage-based gate you own, not just this
one. That slide is worth keeping after the bug is fixed.

**Objection you will get:** *"Can we use this in CI instead of AWS Secrets
Manager?"*

**Answer:** No. CI pulling from a vault needs the master password plus a token —
a human credential in a pipeline. Machine identities are item 1 on the roadmap
and until they ship, the cloud half is developer-local.

**Correct, if it comes up:** `migrate` **generates commands**. Eight of nine
destinations contact nothing; only `github-actions` transfers.

---

## PHP agency — Laravel, Symfony, freelancers

**Deck:** [`php-agency.tex`](php-agency.tex)

**Open with:** zipping a client's `.env` into an email, live payment keys
included. Every agency has done it this month.

**Lead demo:** one vault per client project, `vault share` to the freelancer,
`vault revoke` at contract end — and say clearly that **revocation re-keys the
vault**, so retained keys cannot open future versions. That is the whole pitch
for this audience and it is genuinely finished.

**Then the two gaps that matter at their scale:**

- No "remove this person from all vaults". With thirty clients, offboarding is a
  list you maintain by hand.
- No debug-in-production rule. Show `APP_DEBUG=true` alongside
  `APP_ENV=production` passing `validate --strict` clean.

**Objection you will get:** *"Our clients ask whether this is secure. What do I
tell them?"*

**Answer:** Give them the two-paragraph version — encrypted on your machine, the
server stores ciphertext it cannot read, sharing uses a post-quantum hybrid wrap
— and then the one honest caveat: recipient public keys come from the server, so
a malicious server could substitute its own. Agencies get this question from
non-technical clients constantly; a clean answer with one caveat is worth more
than a marketing sentence.

**Show the Symfony false positive.** `validate --env-name local` reports
`APP_ENV` missing when `.env` supplies it — evnx has no model of layered config.
If you hide it, the Symfony person in the room finds it in ten minutes.

---

## Mobile — Expo, Flutter, EAS

**Deck:** [`mobile.tex`](mobile.tex)

**Open with the rule, not a demo:** *the vault for an app build should contain
only values that are safe to be public.* An APK is a zip file. If the room
rejects this, nothing later helps; if they accept it, the rest is logistics.

**Lead demo:** one vault per flavour, and `cloud run -- bundle exec fastlane
android release` — the keystore password stops being a single point of failure
on someone's laptop. Clean win, unblocks releases.

**Then the trap, which is the best one in any of the seven decks:**
`convert --to json --exclude "*_SECRET*"` is the documented recipe for Flutter's
`--dart-define-from-file`. Show the output. `ANDROID_KEYSTORE_PASSWORD` does not
match `*_SECRET*`, so it went straight into the file that gets compiled into the
app. **The recommended command is the one that leaked it.**

Then give them the fix: `--include "EXPO_PUBLIC_*"`. Name what may be public.
Never enumerate what may not.

**Objection you will get:** *"Firebase keys get flagged and they're supposed to
be public."*

**Answer:** Correct, and evnx cannot tell the difference. Suppress it
deliberately rather than turning the check off. Then make the general point:
name-based and entropy-based detection cannot distinguish "public by design"
from "leaked" — that judgement stays with you, and a tool claiming otherwise
would be lying.

---

## Questions that come up in every room

**"Is this just dotenv-vault / Doppler / Infisical?"**
The distinguishing claims are the zero-knowledge model (the server holds
ciphertext, with a hybrid post-quantum wrap for shares) and the CLI half working
with no account at all — `validate`, `scan`, `diff`, `doctor`, `convert`,
`migrate` are all local. Say which half they are evaluating.

**"What if evnx the company disappears?"**
The CLI is MIT, the server is open source, blobs are AES-256-GCM with a
documented format, and `cloud pull` writes an ordinary `.env`. The exit is
`evnx cloud pull`.

**"Does it work offline?"**
Everything except the `cloud` and `vault` commands.

**"Why is it Rust?"**
Because it ships as one static binary with no runtime, through the packaging
channels your team already uses, and starts fast enough to sit in a pre-commit
hook. If that is not a
constraint you have, the language is not the reason to pick it.

**"What is it bad at?"**
Have an answer ready per room. If you do not, the deck failed at step 4.
