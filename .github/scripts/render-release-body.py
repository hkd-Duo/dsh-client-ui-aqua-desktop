#!/usr/bin/env python3
"""Render .github/release-body.md into /tmp/release-body.md.

Placeholders:
  {{VERSION}} - version from package.json
  {{TAG}}     - release tag (defaults to GITHUB_REF_NAME)
  {{REPO}}    - owner/repo (defaults to GITHUB_REPOSITORY)

Used by both the release workflow (new tags) and the release-notes sync
workflow (keeps the newest release in step with the template).
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_REPO = "hkd-Duo/dsh-client-ui-aqua-desktop"


def render(tag: str, out: pathlib.Path) -> tuple[str, str]:
    version = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    repo = os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPO)
    text = (ROOT / ".github" / "release-body.md").read_text(encoding="utf-8")
    text = text.replace("{{VERSION}}", version).replace("{{TAG}}", tag).replace("{{REPO}}", repo)
    out.write_text(text, encoding="utf-8")
    return tag, version


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default=os.environ.get("GITHUB_REF_NAME", ""))
    ap.add_argument("--out", default="/tmp/release-body.md")
    args = ap.parse_args()

    tag = args.tag or "dev"
    out = pathlib.Path(args.out)
    rendered_tag, version = render(tag, out)
    print(f"rendered {out} for tag={rendered_tag} version={version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
