"""
Cache-bust CSS/JS URLs in live HTML by content hash.
Usage: python _tools/bump-asset-hashes.py [--all]
  --all  also update Archive/**/*.html

Lives under _tools/ so GitHub Pages (Jekyll) will not publish it.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE_ARCHIVE = "--all" in sys.argv

ASSETS = [
    ("style.css", "href"),
    ("colorbox.css", "href"),
    ("sidebar-loader.js", "src"),
]


def short_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def list_html_files() -> list[Path]:
    files = sorted(ROOT.glob("*.html"))
    if INCLUDE_ARCHIVE:
        files.extend(sorted((ROOT / "Archive").rglob("*.html")))
    return files


def main() -> None:
    import re

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
        if text != before:
            html_path.write_text(text, encoding="utf-8", newline="\n")
            changed += 1
            print(f"updated {html_path.relative_to(ROOT)}")

    print(f"Done. {changed} HTML file(s) updated." if changed else "No HTML changes needed.")


if __name__ == "__main__":
    main()
