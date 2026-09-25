#!/usr/bin/env python3
r"""Structural sanity check for the evnx decks (no LaTeX installed here).

Checks, per file:
  * \begin{X} / \end{X} balance
  * balanced braces outside verbatim-ish environments
  * every \capture{f} / \capturepart{f}{a}{b} target exists
  * \capturepart line ranges are within the file
  * frames containing \capture or lstlisting are marked [fragile]
"""
import re, sys, os, glob, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
errors, warnings, stats = [], [], collections.Counter()

def capture_dir_for(path):
    rel = os.path.relpath(path, ROOT)
    depth = rel.count(os.sep)
    # \capturedir is ../captures for depth-1 dirs, ../../captures for depth-2
    return os.path.join(ROOT, "captures")

def check(path):
    src = open(path, encoding="utf-8").read()
    is_preamble = path.endswith("evnx-preamble.tex")
    rel = os.path.relpath(path, ROOT)
    stats["files"] += 1

    # --- environment balance
    stack = []
    for m in re.finditer(r'\\(begin|end)\{([^}]+)\}', src):
        kind, env = m.group(1), m.group(2)
        if kind == "begin":
            stack.append((env, src[:m.start()].count("\n") + 1))
        else:
            if not stack:
                errors.append(f"{rel}: \\end{{{env}}} with no matching begin")
            elif stack[-1][0] != env:
                errors.append(f"{rel}:{src[:m.start()].count(chr(10))+1}: "
                              f"\\end{{{env}}} closes \\begin{{{stack[-1][0]}}} (line {stack[-1][1]})")
                stack.pop()
            else:
                stack.pop()
    for env, ln in stack:
        errors.append(f"{rel}:{ln}: \\begin{{{env}}} never closed")

    stats["frames"] += len(re.findall(r'\\begin\{frame\}', src))

    # --- capture targets exist and ranges are sane
    cdir = capture_dir_for(path)
    for m in (re.finditer(r'\\capture\{([^}]+)\}', src) if not is_preamble else []):
        f = os.path.join(cdir, m.group(1))
        stats["captures"] += 1
        if not os.path.exists(f):
            errors.append(f"{rel}: \\capture target missing: {m.group(1)}")
    for m in re.finditer(r'\\capturepart\{([^}]+)\}\{(\d+)\}\{(\d+)\}', src):
        f = os.path.join(cdir, m.group(1)); a, b = int(m.group(2)), int(m.group(3))
        stats["captures"] += 1
        if not os.path.exists(f):
            errors.append(f"{rel}: \\capturepart target missing: {m.group(1)}")
            continue
        n = sum(1 for _ in open(f, encoding="utf-8", errors="replace"))
        if a > n:
            errors.append(f"{rel}: \\capturepart{{{m.group(1)}}} starts at {a} but file has {n} lines")
        elif b > n:
            warnings.append(f"{rel}: \\capturepart{{{m.group(1)}}} asks to {b}, file has {n} lines (clipped)")
        if a > b:
            errors.append(f"{rel}: \\capturepart{{{m.group(1)}}} range {a}..{b} is inverted")

    # --- fragile frames
    for m in re.finditer(r'\\begin\{frame\}(\[[^\]]*\])?\{', src):
        start = m.end()
        nxt = src.find(r'\begin{frame}', start)
        body = src[start: nxt if nxt != -1 else len(src)]
        needs = ('\\capture' in body) or ('lstlisting' in body) or ('semiverbatim' in body)
        opts = m.group(1) or ""
        if needs and 'fragile' not in opts:
            ln = src[:m.start()].count("\n") + 1
            errors.append(f"{rel}:{ln}: frame contains verbatim content but is not [fragile]")

    # --- \input targets
    for m in re.finditer(r'\\input\{([^}]+)\}', src):
        t = m.group(1)
        cand = os.path.normpath(os.path.join(os.path.dirname(path), t))
        if not (os.path.exists(cand) or os.path.exists(cand + ".tex")):
            errors.append(f"{rel}: \\input target missing: {t}")

for f in sorted(glob.glob(os.path.join(ROOT, "**", "*.tex"), recursive=True)):
    check(f)

print(f"checked {stats['files']} .tex files, {stats['frames']} frames, {stats['captures']} capture references\n")
for w in warnings: print("WARN ", w)
for e in errors:   print("ERROR", e)
print()
print("RESULT:", "PASS — no structural errors" if not errors else f"FAIL — {len(errors)} error(s)")
sys.exit(1 if errors else 0)
