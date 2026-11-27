#!/usr/bin/env python3
"""Validate the public organization profile and its referenced assets."""

from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profile" / "README.md"
REQUIRED_ASSETS = [
    ROOT / "assets" / "github-banner.svg",
    ROOT / "assets" / "avatar-512.png",
    ROOT / "assets" / "social-preview-1280x640.png",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


if not PROFILE.is_file() or not PROFILE.read_text(encoding="utf-8").strip():
    fail("profile/README.md is missing or empty")

readme = PROFILE.read_text(encoding="utf-8")
if "../assets/github-banner.svg" not in readme:
    fail("profile/README.md does not reference the profile banner")

for asset in REQUIRED_ASSETS:
    if not asset.is_file() or asset.stat().st_size == 0:
        fail(f"required asset is missing or empty: {asset.relative_to(ROOT)}")

for svg in sorted((ROOT / "assets").glob("*.svg")):
    try:
        ET.parse(svg)
    except ET.ParseError as exc:
        fail(f"invalid SVG XML: {svg.relative_to(ROOT)}: {exc}")

for png in sorted((ROOT / "assets").glob("*.png")):
    if png.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"invalid PNG signature: {png.relative_to(ROOT)}")

print(
    f"Validated profile README, {len(REQUIRED_ASSETS)} required assets, "
    f"{len(list((ROOT / 'assets').glob('*.svg')))} SVG files, and PNG signatures."
)
