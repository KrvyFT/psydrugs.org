#!/usr/bin/env python3
"""为 chemical_aterials 文件添加 YAML front matter"""
import os
import re
from datetime import datetime

def extract_title(content):
    """从文件内容中提取标题"""
    # 查找 # 标题行
    match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Unknown"

def add_frontmatter(filepath):
    """为文件添加 YAML front matter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 跳过已有 front matter 的文件
    if content.startswith('---'):
        return False
    
    # 提取标题
    title = extract_title(content)
    
    # 生成 front matter
    frontmatter = f"""---
wiki: drugs
title: {title}
description: 化学物质
published: true
date: {datetime.now().isoformat()}Z
tags: 
editor: markdown
updated: {datetime.now().isoformat()}Z
---

"""
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    
    return True

def main():
    base_dir = '/home/krvy/psydrugs.org/source/drugs/chemical_aterials'
    count = 0
    
    for filename in sorted(os.listdir(base_dir)):
        if filename.endswith('.md'):
            filepath = os.path.join(base_dir, filename)
            if add_frontmatter(filepath):
                print(f"✓ 已添加: {filename}")
                count += 1
            else:
                print(f"~ 已跳过: {filename} (已有 front matter)")
    
    print(f"\n处理完成！添加 front matter 的文件数: {count}")

if __name__ == '__main__':
    main()
