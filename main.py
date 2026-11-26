#!/usr/bin/env python3
"""Write the make.fun entry text for 'The Moon Gets One Star'.

Deterministic: no network, no randomness, no clock. Writes the fixed
one-star review of the Moon to <output-dir>/entry.txt (default /output),
with no trailing newline.
"""

import os
import sys

ENTRY_TEXT = (
    "One star. Turns my neighbours into werewolves once a month "
    "and acts innocent. Zero remorse, zero refund."
)


def main(argv):
    output_dir = "/output"
    if len(argv) > 1:
        output_dir = argv[1]
    elif os.environ.get("OUTPUT_DIR"):
        output_dir = os.environ["OUTPUT_DIR"]
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY_TEXT)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
