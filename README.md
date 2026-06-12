# Deyta Homebrew tap

Homebrew formulae for [Deyta](https://github.com/DeytaHQ) tools.

## Install

```bash
brew install DeytaHQ/deyta/deyta
```

Or tap first, then install:

```bash
brew tap DeytaHQ/deyta
brew install deyta
```

Upgrade with `brew upgrade deyta`.

## What this installs

`deyta` is a Python CLI. The formula creates an isolated virtualenv (on
`python@3.13`) and installs the published `deyta-cli` wheel and its dependencies
from PyPI. It uses prebuilt wheels for the heavy native dependencies (`pyarrow`,
`lancedb`, `numpy`, `tokenizers`), so no Rust/C++ toolchain is needed. Because it
fetches from PyPI at install time, the formula declares `allow_network_access!`
and is distributed here as a tap rather than in homebrew-core.

> Note: `deyta` needs `OPENAI_API_KEY` in your environment at runtime (Khora uses
> it for embeddings and entity extraction). Docker is only needed for the
> `postgres` backend.

## Maintaining

The formula's `url` and `sha256` are pinned to a PyPI source distribution and
bumped on each release:

- **Automatically** — the `deyta-cli` release workflow dispatches a
  `bump-formula` event here after publishing to PyPI (requires a
  `HOMEBREW_TAP_TOKEN` secret on the `deyta-cli` repo with `contents:write` here).
- **Manually** — run the *Bump formula* workflow, or locally:

  ```bash
  python3 scripts/update-formula.py        # latest on PyPI
  python3 scripts/update-formula.py 0.2.0  # a specific version
  git commit -am "deyta 0.2.0" && git push
  ```

Test a formula change locally before pushing:

```bash
brew install --build-from-source ./Formula/deyta.rb
brew test deyta
brew audit --strict --online deyta   # `allow_network_access!` warning is expected for a tap
```
