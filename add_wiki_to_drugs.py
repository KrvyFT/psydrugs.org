#!/usr/bin/env python3
"""Add wiki: drugs to all drugs markdown files if missing"""
import os
import re
from pathlib import Path

root = Path('/home/krvy/Psydrugs.icu/source/drugs')
files = list(root.rglob('*.md'))
updated = 0
skipped = 0

for fp in files:
    text = fp.read_text(encoding='utf-8')
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not m:
        skipped += 1
        continue
    front = m.group(1)
    if re.search(r'^wiki:\s*drugs\b', front, re.MULTILINE):
        skipped += 1
        continue
    # insert wiki: drugs after first line in frontmatter
    lines = front.split('\n')
    if lines and lines[0].strip() == '':
        insert_at = 1
    else:
        insert_at = 0
    new_front = lines[:insert_at] + ['wiki: drugs'] + lines[insert_at:]
    new_front_text = '\n'.join(new_front)
    new_text = f"---\n{new_front_text}\n---\n" + text[m.end():]
    fp.write_text(new_text, encoding='utf-8')
    updated += 1
    print(f"added wiki to {fp.relative_to(root)}")

print(f"done. updated={updated} skipped={skipped} total={len(files)}")
