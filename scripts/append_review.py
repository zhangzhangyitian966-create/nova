#!/usr/bin/env python3
"""Append a code review entry to the review log file."""

import sys
import os
from datetime import datetime

REVIEW_LOG = ".reviews.md"


def main():
    if len(sys.argv) < 2:
        print("Usage: append_review.py <title>", file=sys.stderr)
        sys.exit(1)

    title = sys.argv[1]
    content = sys.stdin.read()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"\n---\n\n## {title}\n\n*Reviewed: {timestamp}*\n\n{content}\n"



    with open(REVIEW_LOG, "a") as f:
        f.write(entry)

    print(f"Review appended to {REVIEW_LOG}")


if __name__ == "__main__":
    main()
