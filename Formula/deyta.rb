class Deyta < Formula
  include Language::Python::Virtualenv

  desc "Unified CLI for Deyta's services (wraps Khora persistent memory for AI agents)"
  homepage "https://github.com/DeytaHQ/deyta-cli"
  # url + sha256 point at the PyPI source distribution and are updated on each
  # release by scripts/update-formula.py (see .github/workflows/bump-formula.yml).
  url "https://files.pythonhosted.org/packages/source/d/deyta-cli/deyta_cli-0.0.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  depends_on "python@3.13"

  # The dependency tree includes heavy native packages (pyarrow, lancedb, numpy,
  # tokenizers, pydantic-core). Building those from source under Homebrew would
  # need a Rust + Arrow C++ toolchain. Instead we install the published wheels
  # from PyPI into an isolated virtualenv, which requires network access at
  # build time. (This is why the formula lives in a tap, not homebrew-core.)
  allow_network_access! :build

  def install
    virtualenv_create(libexec, "python3.13")
    system libexec/"bin/pip", "install", "--disable-pip-version-check",
           "--no-cache-dir", "deyta-cli==#{version}"
    bin.install_symlink libexec/"bin/deyta"
  end

  test do
    # --help imports only the CLI layer (never Khora) and needs no network.
    assert_match "deyta", shell_output("#{bin}/deyta --help")
  end
end
