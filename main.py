#!/usr/bin/env python3
"""Write the make.fun entry text for 'The Moon Gets One Star'.

Deterministic: no network, no randomness, no clock. Writes the fixed
one-star review of the Moon to <output-dir>/entry.txt (default /output),
with no trailing newline.
"""

import os
import sys
import tempfile

ENTRY_TEXT = (
    "One star. Turns my neighbours into werewolves once a month "
    "and acts innocent. Zero remorse, zero refund."
)


def write_entry(path):
    """Write ENTRY_TEXT atomically, then verify the bytes on disk.

    Writes to a temp file in the same directory and renames it into
    place, so a failed run never leaves a half-written entry.txt.
    Returns True only if the file on disk is byte-identical to
    ENTRY_TEXT; raises OSError on any write/verify failure.
    """
    directory = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(prefix=".entry-", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY_TEXT)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    with open(path, "rb") as f:
        if f.read() != ENTRY_TEXT.encode("utf-8"):
            raise OSError(f"verification failed: {path} does not match ENTRY_TEXT")
    return True


def main(argv):
    output_dir = "/output"
    if len(argv) > 1:
        output_dir = argv[1]
    elif os.environ.get("OUTPUT_DIR"):
        output_dir = os.environ["OUTPUT_DIR"]
    if not output_dir:
        print("error: output directory must not be empty", file=sys.stderr)
        return 2
    if os.path.isfile(output_dir):
        print(f"error: output path {output_dir!r} is a file, not a directory",
              file=sys.stderr)
        return 2
    try:
        os.makedirs(output_dir, exist_ok=True)
        write_entry(os.path.join(output_dir, "entry.txt"))
    except OSError as exc:
        print(f"error: cannot write entry: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
