"""
Cache-bust CSS/JS URLs in live HTML by content hash.
Bump human-readable site build id (CalVer YYYY.MM.DD.N) in HTML markers.

Usage: python _tools/bump-asset-hashes.py [--all]
  --all  also update Archive/**/*.html

Lives under _tools/ so GitHub Pages (Jekyll) will not publish it.
"""
from __future__ import annotations

import hashlib
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = Path(__file__).resolve().parent / "site-version.txt"
INCLUDE_ARCHIVE = "--all" in sys.argv

ASSETS = [
    ("style.css", "href"),
    ("colorbox.css", "href"),
    ("sidebar-loader.js", "src"),
]

BUILD_COMMENT = re.compile(r"<!--\s*iancw-build:\s*[^>]*-->")
BUILD_META = re.compile(r'<meta\s+name="site-version"\s+content="[^"]*"\s*/?>')
BODY_BUILD = re.compile(r'(<body\b[^>]*)\s+data-build="[^"]*"')
BODY_OPEN = re.compile(r"(<body\b[^>]*)(>)")


def short_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def list_html_files() -> list[Path]:
    files = sorted(ROOT.glob("*.html"))
    if INCLUDE_ARCHIVE:
        files.extend(sorted((ROOT / "Archive").rglob("*.html")))
    return files


def next_site_version(current: str) -> str:
    today = date.today().strftime("%Y.%m.%d")
    current = current.strip()
    if current.startswith(f"{today}."):
        seq = int(current.rsplit(".", 1)[1])
        return f"{today}.{seq + 1}"
    return f"{today}.1"


def read_site_version() -> str:
    if VERSION_FILE.is_file():
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    return next_site_version("")


def bump_site_version() -> str:
    version = next_site_version(read_site_version())
    VERSION_FILE.write_text(f"{version}\n", encoding="utf-8", newline="\n")
    return version


def apply_site_version(text: str, version: str) -> str:
    comment = f"<!-- iancw-build: {version} -->"
    meta = f'<meta name="site-version" content="{version}">'

    if BUILD_COMMENT.search(text):
        text = BUILD_COMMENT.sub(comment, text)
    else:
        text = re.sub(
            r'(\s*<meta\s+charset="utf-8"\s*/?>)',
            rf"\n\t\t{comment}\n\t\t{meta}\n\t\t<meta charset=\"utf-8\">",
            text,
            count=1,
            flags=re.IGNORECASE,
        )

    if BUILD_META.search(text):
        text = BUILD_META.sub(meta, text)

    if BODY_BUILD.search(text):
        text = BODY_BUILD.sub(rf'\1 data-build="{version}"', text)
    else:
        text = BODY_OPEN.sub(rf'\1 data-build="{version}"\2', text, count=1)

    return text


def main() -> None:
    site_version = bump_site_version()
    print(f"site-version -> {site_version}")

    hashes: dict[str, str] = {}
    for name, _attr in ASSETS:
        fp = ROOT / name
        if not fp.is_file():
            print(f"skip missing {name}")
            continue
        hashes[name] = short_hash(fp)
        print(f"{name} -> {hashes[name]}")

    changed = 0
    for html_path in list_html_files():
        text = html_path.read_text(encoding="utf-8")
        before = text
        for name, attr in ASSETS:
            h = hashes.get(name)
            if not h:
                continue
            esc = re.escape(name)
            pattern = re.compile(
                rf'({attr}\s*=\s*"){esc}(?:\?[^"]*)?(")',
                re.IGNORECASE,
            )
            text = pattern.sub(rf"\1{name}?v={h}\2", text)
        text = apply_site_version(text, site_version)
        if text != before:
            html_path.write_text(text, encoding="utf-8", newline="\n")
            changed += 1
            print(f"updated {html_path.relative_to(ROOT)}")

    print(f"Done. {changed} HTML file(s) updated." if changed else "No HTML changes needed.")


if __name__ == "__main__":
    main()
