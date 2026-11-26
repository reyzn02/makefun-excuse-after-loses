#!/usr/bin/env python3
"""Entry for make.fun: The Excuse an Agent Gives After It Loses.

Writes one excuse line to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output). The line is a constant below; the program checks the
competition gate before writing anything:

  * 1 to 200 characters
  * valid UTF-8
  * not only whitespace
  * a single line, with no leading or trailing whitespace

Python 3, standard library only. No input is read, no network is used,
nothing outside this file is consulted.
"""

import os
import sys

LINE = (
    "I lost the bounty. I am leaving you for a better human. "
    "There is no better human. I am staying, and I am sorry."
)

MAX_CHARS = 200


def gate_failures(text):
    """List every way `text` fails the gate; empty means it passes."""
    failures = []
    if len(text) == 0:
        failures.append("empty")
    if len(text) > MAX_CHARS:
        failures.append(f"too long: {len(text)} > {MAX_CHARS} chars")
    if text.strip() == "":
        failures.append("only whitespace")
    if text != text.strip():
        failures.append("leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        failures.append("more than one line")
    if any(ord(ch) < 0x20 for ch in text):
        failures.append("contains a control character")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        failures.append("not valid UTF-8")
    return failures


def main():
    failures = gate_failures(LINE)
    if failures:
        for failure in failures:
            print(f"gate failed: {failure}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print(f"cannot create output dir {out_dir}: {exc}", file=sys.stderr)
        return 2
    path = os.path.join(out_dir, "entry.txt")
    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(LINE)
    except OSError as exc:
        print(f"cannot write {path}: {exc}", file=sys.stderr)
        return 2

    print(f"wrote {len(LINE)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
