#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将药物文件名从英文代码改为中文名，并修正所有引用
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def get_drug_mapping():
    """读取所有 markdown 文件并建立编码到中文名的映射"""
    mapping = {}
    drugs_dir = Path("./source/drugs")
    
    for md_file in sorted(drugs_dir.glob("*.md")):
        if md_file.name not in ["index.md", "compound.md", "introduction-to-overdose.md", "new-page.md"]:
            code = md_file.stem
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'^title: (.+)$', content, re.MULTILINE)
                if match:
                    title = match.group(1).strip()
                    mapping[code] = title
    
    return mapping

def find_all_references(mapping):
    """找到所有引用这些药物代码的文件"""
    references = defaultdict(list)
    pattern = '|'.join(re.escape(code) for code in mapping.keys())
    
    # 需要搜索的文件类型
    for root, dirs, files in os.walk("./source"):
        # 跳过某些目录
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules']]
        
        for file in files:
            if file.endswith(('.md', '.html', '.yml')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for match in re.finditer(pattern, content):
                            code = match.group(0)
                            references[code].append(filepath)
                except:
                    pass
    
    return references

def rename_files(mapping):
    """重命名所有药物文件"""
    drugs_dir = Path("./source/drugs")
    
    for code, title in mapping.items():
        old_path = drugs_dir / f"{code}.md"
        new_path = drugs_dir / f"{title}.md"
        
        if old_path.exists() and not new_path.exists():
            old_path.rename(new_path)
            print(f"✓ 重命名: {code}.md -> {title}.md")
        elif new_path.exists():
            print(f"⚠ 跳过: {title}.md 已存在")
        else:
            print(f"✗ 未找到: {code}.md")

def update_references(mapping):
    """更新所有引用"""
    count = 0
    
    # 更新 source/_data/wiki/drugs.yml
    drugs_yml = Path("./source/_data/wiki/drugs.yml")
    if drugs_yml.exists():
        content = drugs_yml.read_text(encoding='utf-8')
        original_content = content
        
        for code, title in mapping.items():
            # 替换引用 (需要保持缩进和格式)
            content = re.sub(
                rf'(\s+)- {re.escape(code)}(\s|$)',
                rf'\1- {title}\2',
                content
            )
        
        if content != original_content:
            drugs_yml.write_text(content, encoding='utf-8')
            print(f"✓ 更新: source/_data/wiki/drugs.yml")

    # 更新所有 markdown 和 html 文件中的链接
    for root, dirs, files in os.walk("./source"):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules']]
        
        for file in files:
            if file.endswith(('.md', '.html')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    for code, title in mapping.items():
                        # 替换各种链接格式
                        # [text](/drugs/CODE) -> [text](/drugs/TITLE)
                        content = re.sub(
                            rf'(?<=/drugs/){re.escape(code)}(?=/|\)|\")',
                            title,
                            content
                        )
                        # CODE/xxx -> TITLE/xxx
                        content = re.sub(
                            rf'^(\s*- ){re.escape(code)}/([^/\s]+)',
                            rf'\1{title}/\2',
                            content,
                            flags=re.MULTILINE
                        )
                    
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"✓ 更新: {filepath}")
                        count += 1
                except Exception as e:
                    print(f"✗ 错误处理 {filepath}: {e}")
    
    return count

def main():
    print("=" * 60)
    print("药物文件名称重命名工具")
    print("=" * 60)
    
    # 获取映射
    print("\n1. 读取药物文件映射...")
    mapping = get_drug_mapping()
    print(f"   找到 {len(mapping)} 个药物文件")
    
    # 显示前几个映射
    print("\n   示例映射:")
    for i, (code, title) in enumerate(list(mapping.items())[:5]):
        print(f"   - {code:10} -> {title}")
    
    # 询问确认
    response = input("\n2. 是否开始重命名文件? (y/n): ")
    if response.lower() != 'y':
        print("取消操作")
        return
    
    # 重命名文件
    print("\n3. 重命名文件...")
    rename_files(mapping)
    
    # 更新引用
    print("\n4. 更新所有引用...")
    count = update_references(mapping)
    print(f"   共更新 {count} 个文件")
    
    print("\n" + "=" * 60)
    print("完成！")
    print("请运行: hexo clean && hexo g")
    print("=" * 60)

if __name__ == "__main__":
    main()
