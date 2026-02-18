#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


SPLIT_RE = re.compile(r"[、,，;/；]+")


def split_values(value: str) -> list[str]:
    parts = [p.strip() for p in SPLIT_RE.split(value) if p.strip()]
    cleaned: list[str] = []
    for part in parts:
        cleaned_part = part.strip("'\"")
        if cleaned_part and cleaned_part not in cleaned:
            cleaned.append(cleaned_part)
    return cleaned


def parse_tags_value(value: str) -> list[str]:
    if not value:
        return []
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]
    return split_values(value)


def format_tags(items: list[str]) -> str:
    return f"[{', '.join(items)}]"


def update_frontmatter(lines: list[str]) -> tuple[list[str], bool]:
    desc_idx = next((i for i, line in enumerate(lines) if line.startswith("description:")), None)
    if desc_idx is None:
        return lines, False

    desc_value = lines[desc_idx].split(":", 1)[1].strip()
    if not desc_value:
        return lines, False

    desc_items = split_values(desc_value)
    if not desc_items:
        return lines, False

    tags_idx = next((i for i, line in enumerate(lines) if line.startswith("tags:")), None)
    if tags_idx is None:
        insert_idx = desc_idx + 1
        lines.insert(insert_idx, f"tags: {format_tags(desc_items)}")
        return lines, True

    tags_value = lines[tags_idx].split(":", 1)[1].strip()
    existing = parse_tags_value(tags_value)
    merged = existing + [item for item in desc_items if item not in existing]
    lines[tags_idx] = f"tags: {format_tags(merged)}"
    return lines, True


def process_file(path: Path, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False

    end_idx = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end_idx is None:
        return False

    frontmatter = lines[1:end_idx]
    body = lines[end_idx + 1 :]

    updated_frontmatter, changed = update_frontmatter(frontmatter)
    if not changed:
        return False

    new_text = "\n".join(["---", *updated_frontmatter, "---", *body])
    if not new_text.endswith("\n") and text.endswith("\n"):
        new_text += "\n"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync description values into tags for drug pages.")
    parser.add_argument(
        "--root",
        default="source/drugs",
        help="Root directory to scan (default: source/drugs)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not modify files")
    parser.add_argument("--verbose", action="store_true", help="Print each updated file")
    args = parser.parse_args()

    root = Path(args.root)
    updated = 0
    for path in root.rglob("*.md"):
        if process_file(path, args.dry_run):
            updated += 1
            if args.verbose:
                print(path.as_posix())

    print(f"Updated {updated} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
