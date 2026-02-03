#!/usr/bin/env python3
"""
验证和修复drugs文件的front-matter
确保所有drugs文件都有正确的metadata
"""
import os
import re
from datetime import datetime

def get_frontmatter_from_file(filepath):
    """从文件中提取front-matter"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 匹配YAML frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            return match.group(1)
        
        # 如果没有frontmatter，返回None
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def ensure_frontmatter(filepath, drug_name):
    """确保文件有基本的front-matter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有front-matter
    if content.startswith('---'):
        return False  # 已有front-matter
    
    # 创建基础front-matter
    frontmatter = f"""---
title: {drug_name}
description: 
published: true
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')}
tags: 
editor: markdown
updated: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')}
---

"""
    
    # 添加front-matter到文件开头
    new_content = frontmatter + content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def validate_drugs():
    """验证所有drugs文件"""
    drugs_dir = '/home/krvy/Psydrugs.icu/source/drugs'
    stats = {
        'total': 0,
        'with_frontmatter': 0,
        'without_frontmatter': 0,
        'added_frontmatter': 0,
        'issues': []
    }
    
    for filename in sorted(os.listdir(drugs_dir)):
        if filename.endswith('.md'):
            filepath = os.path.join(drugs_dir, filename)
            drug_name = filename.replace('.md', '')
            
            stats['total'] += 1
            
            # 检查是否是一级文件（不是子目录中的文件）
            if os.path.isfile(filepath):
                frontmatter = get_frontmatter_from_file(filepath)
                
                if frontmatter:
                    stats['with_frontmatter'] += 1
                else:
                    stats['without_frontmatter'] += 1
                    # 尝试添加front-matter
                    if ensure_frontmatter(filepath, drug_name):
                        stats['added_frontmatter'] += 1
                        print(f"✓ 为 {drug_name} 添加了front-matter")
    
    # 打印统计信息
    print("\n=== Drugs 文件验证报告 ===")
    print(f"总文件数: {stats['total']}")
    print(f"已有front-matter: {stats['with_frontmatter']}")
    print(f"缺少front-matter: {stats['without_frontmatter']}")
    print(f"新增front-matter: {stats['added_frontmatter']}")
    
    if stats['issues']:
        print(f"\n问题列表:")
        for issue in stats['issues']:
            print(f"  - {issue}")
    else:
        print("\n✓ 所有drugs文件验证完毕，无问题")

if __name__ == '__main__':
    validate_drugs()
