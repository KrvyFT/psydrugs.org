#!/usr/bin/env python3
import os
import re
from datetime import datetime

def convert_frontmatter(content, filename):
    # 提取原始 front-matter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return content
    
    frontmatter = match.group(1)
    body = match.group(2)
    
    # 解析字段
    title = re.search(r'title:\s*(.+)', frontmatter)
    date = re.search(r'date:\s*(.+)', frontmatter)
    date_created = re.search(r'updated:\s*(.+)', frontmatter)
    
    title_text = title.group(1).strip() if title else filename.replace('.md', '')
    
    # 使用 updated 作为 date，date 作为 updated
    if date_created:
        date_str = date_created.group(1).strip()
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        date_formatted = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        date_formatted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    updated_str = ''
    if date:
        date_str = date.group(1).strip()
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        updated_formatted = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        updated_str = f'\nupdated: {updated_formatted}'
    
    # 构建新的 front-matter
    new_frontmatter = f'''---
layout: wiki
wiki: reports
title: {title_text}
date: {date_formatted}{updated_str}
---
'''
    
    return new_frontmatter + '\n' + body

# 处理所有 RP 文件
rp_dir = '/home/krvy/safeoverwiki/RP'
count = 0
for filename in sorted(os.listdir(rp_dir)):
    if filename.endswith('.md'):
        filepath = os.path.join(rp_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = convert_frontmatter(content, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        count += 1
        print(f'已转换: {filename}')

print(f'\n转换完成！共处理 {count} 个文件')
