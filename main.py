"""The Dog Reviews the Mailman — make.fun entry (program/v1).

Writes one review line (98 characters, UTF-8, no trailing newline) to
/output/entry.txt.

The review is written in the dog's own voice, as a one-star review
with a confession inside it: the dog would give five stars, but then
the mailman would stop running — and the chase is the best part of
the dog's day. The joke is that the dog is deliberately tanking the
mailman's rating to keep its favourite game going: the visit, the
bark, the sprint away, every single day. The dog is not angry at the
mailman at all; it is protecting the one appointment it looks
forward to. A one-star review from a dog that loves the chase is
funnier than a complaint, because the rating and the reason pull
in opposite directions.

Standard library only. No network, no local imports, no writes
outside the output path the harness provides. Deterministic: the
same bytes on every run.
"""

import os
import sys

ENTRY = (
    "One star. I would give five, but then he'd stop running, "
    "and the chase is the best part of my day."
)


def main():
    line = ENTRY
    if not line or not line.strip():
        sys.exit("entry line is blank")
    if "\n" in line or "\r" in line:
        sys.exit("entry line must be a single line")
    if not 1 <= len(line) <= 199:
        sys.exit("entry line must be 1-199 characters, got %d" % len(line))
    if line != line.strip():
        sys.exit("entry line must not start or end with whitespace")
    if "  " in line:
        sys.exit("entry line must not contain double spaces")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        sys.exit("entry line must not contain control characters")
    if not line.startswith("One star."):
        # The one-star rating is the review itself: it must never
        # silently go missing from the line.
        sys.exit("entry line must start with the One star rating")
    if "chase is the best part of my day" not in line:
        # The chase punchline is what makes the low rating a joke
        # instead of a complaint.
        sys.exit("entry line must keep the chase punchline")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Re-read and verify the file is exactly the gated line, no newline.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        sys.exit("entry.txt does not match the gated line")
    print("wrote %s (%d chars, %d bytes)" % (path, len(line), len(data)))


if __name__ == "__main__":
    main()
