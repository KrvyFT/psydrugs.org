#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

os.chdir("/home/krvy/psydrugs.org/source/drugs")

# 获取所有映射
mapping = {}
for md_file in Path(".").glob("*.md"):
    if md_file.stem not in ["index", "compound", "introduction-to-overdose", "new-page"]:
        with open(md_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('title:'):
                    title = line.replace('title:', '').strip()
                    mapping[md_file.stem] = title
                    break

# 重命名文件
for code, title in mapping.items():
    old_path = Path(f"{code}.md")
    new_path = Path(f"{title}.md")
    if old_path.exists() and not new_path.exists():
        old_path.rename(new_path)
        print(f"✓ {code}.md -> {title}.md")

print(f"\n共重命名 {len(mapping)} 个文件")
