#!/usr/bin/env python3
import os
from pathlib import Path

os.chdir("/home/krvy/psydrugs.org/source/drugs")

# 列出所有 MD 文件并建立映射  
files = {}
for f in sorted(Path(".").glob("*.md")):
    if f.stem not in ["index", "compound", "introduction-to-overdose", "new-page"]:
        with open(f, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('title:'):
                    title = line.replace('title:', '').strip()
                    files[f.stem] = title
                    break

print("所有药物文件映射:")
for code, title in sorted(files.items()):
    if code[0].isupper():
        print(f"{code:15} -> {title}")
