#!/usr/bin/env python3
"""Point Formula/deyta.rb at a given (or the latest) deyta-cli release on PyPI.

Reads the source-distribution URL and sha256 straight from the PyPI JSON API and
rewrites the `url`/`sha256` lines in the formula. Homebrew derives the version
from the sdist filename, so there is no separate version line to update.

Usage:
    python scripts/update-formula.py            # latest version on PyPI
    python scripts/update-formula.py 0.2.0      # a specific version
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

PROJECT = "deyta-cli"
FORMULA = Path(__file__).resolve().parent.parent / "Formula" / "deyta.rb"


def fetch(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as resp:  # noqa: S310 (trusted host)
        return json.load(resp)


def sdist_for(version: str | None) -> tuple[str, str, str]:
    """Return (version, url, sha256) for the sdist of the given/latest version."""
    suffix = f"{PROJECT}/{version}/json" if version else f"{PROJECT}/json"
    data = fetch(f"https://pypi.org/pypi/{suffix}")
    version = data["info"]["version"]
    for f in data["urls"]:
        if f["packagetype"] == "sdist":
            return version, f["url"], f["digests"]["sha256"]
    raise SystemExit(f"No sdist found for {PROJECT} {version}")


def main() -> None:
    version = sys.argv[1] if len(sys.argv) > 1 else None
    version, url, sha256 = sdist_for(version)

    text = FORMULA.read_text()
    text, n_url = re.subn(r'^(\s*url\s+)"[^"]*"', rf'\1"{url}"', text, count=1, flags=re.M)
    text, n_sha = re.subn(r'^(\s*sha256\s+)"[^"]*"', rf'\1"{sha256}"', text, count=1, flags=re.M)
    if n_url != 1 or n_sha != 1:
        raise SystemExit("Could not locate url/sha256 lines in formula")
    FORMULA.write_text(text)

    print(f"Updated {FORMULA.name} -> {PROJECT} {version}")
    print(f"  url:    {url}")
    print(f"  sha256: {sha256}")


if __name__ == "__main__":
    main()
