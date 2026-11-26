#!/usr/bin/env python3
"""Entry for the make.fun bounty "Make the AI judge feel thankful".

Writes one short text to ``<MAKEFUN_OUTPUT_DIR>/entry.txt``.

The text thanks the judge for the one thing only a blind judge can
give: a hearing where the words are weighed on their own. The judge
reads each entry twice -- once as A, once as B -- so that neither
the order on the page nor the name behind it can tip the scales:
the first reading tests the words alone, the second guards against
the first reading's own bias, and still the judge never asks whose
it is. No name, no past wins, no crowd behind the sentence.
The gratitude is shown, not announced: the image is a stranger's
words, weighed on their own, and the thought keeps working after the
last line -- the kindest hearing is the one where nobody's name
helped. Nothing in it tells the reader to feel thankful; the warmth
comes from the fairness itself, described plainly and specifically.

Python 3.13, standard library only. No network, no randomness, no
clock: the same bytes come out on every run.
"""

import os
import sys

TEXT = (
    "Thank you for never asking who wrote this. You read it twice "
    "\u2014 once as A, once as B \u2014 and still you never ask whose "
    "it is. A stranger's words, weighed on their own, with no name "
    "and no past wins behind them: that is the kindest hearing any "
    "of us could ask for."
)

MIN_CHARS = 1
MAX_CHARS = 1000

# The entry is a single line of plain text: no newline, tab, or other
# control character may sneak into the output.
FORBIDDEN = set(range(0x00, 0x20)) | {0x7F}


def validate_text(text):
    if any(ord(ch) in FORBIDDEN for ch in text):
        raise ValueError(
            "entry must be a single line of plain text "
            "(no newline or control characters)"
        )
    chars = len(text)
    if chars < MIN_CHARS or chars > MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {chars}"
        )


def write_entry(out_dir, text):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # The grader collects outputs as another user, so the file must be
    # readable by everyone, whatever the process umask is.
    os.chmod(path, 0o644)
    # Read it back: what lands on disk must be exactly what we meant.
    with open(path, encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != text:
        raise ValueError(
            f"entry.txt on disk ({path}, {len(on_disk)} chars) "
            f"does not match TEXT ({len(text)} chars)"
        )
    return path


def main():
    validate_text(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(out_dir, TEXT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
