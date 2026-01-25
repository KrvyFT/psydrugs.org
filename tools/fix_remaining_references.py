#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第二阶段：更新所有还未转换的英文代码引用为中文名
"""

import os
import re
from pathlib import Path

def get_all_mapping():
    """获取所有文件（包括已转换的）的完整映射"""
    mapping = {}
    drugs_dir = Path("./source/drugs")
    
    # 列出所有文件并建立映射
    for md_file in sorted(drugs_dir.glob("*.md")):
        if md_file.stem not in ["index", "compound", "introduction-to-overdose", "new-page"]:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 查找 title 字段
                match = re.search(r'^title: (.+)$', content, re.MULTILINE)
                if match:
                    title = match.group(1).strip()
                    # 用下划线替代斜杠
                    filename = title.replace('/', '_')
                    mapping[md_file.stem] = {
                        'title': title,
                        'filename': filename
                    }
    
    return mapping

def fix_yaml_references(mapping):
    """修复 YAML 文件中的所有引用"""
    yml_path = Path("./source/_data/wiki/drugs.yml")
    content = yml_path.read_text(encoding='utf-8')
    original = content
    
    # 按照题目字符数从长到短排序，避免短代码误匹配
    sorted_codes = sorted(mapping.keys(), key=len, reverse=True)
    
    for code in sorted_codes:
        info = mapping[code]
        # 替换 - CODE 格式的行
        # 使用更严格的匹配，确保是独立的单词
        content = re.sub(
            rf'^(\s+)- {re.escape(code)}($)',
            rf'\1- {info["filename"]}',
            content,
            flags=re.MULTILINE
        )
    
    if content != original:
        yml_path.write_text(content, encoding='utf-8')
        print(f"✓ 修复 source/_data/wiki/drugs.yml")
        return True
    else:
        print("✗ source/_data/wiki/drugs.yml 没有需要修改的内容")
    return False

def fix_markdown_references(mapping):
    """修复所有 markdown 文件中的引用"""
    updated_count = 0
    
    sorted_codes = sorted(mapping.keys(), key=len, reverse=True)
    
    for root, dirs, files in os.walk("./source"):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules']]
        
        for file in files:
            if file.endswith('.md'):
                filepath = Path(root) / file
                
                try:
                    content = filepath.read_text(encoding='utf-8')
                    original = content
                    
                    for code in sorted_codes:
                        info = mapping[code]
                        
                        # 替换各种格式的引用
                        # 1. 链接格式：[text](/drugs/CODE) -> [text](/drugs/FILENAME)
                        content = re.sub(
                            rf'(/drugs/){re.escape(code)}(?=/|\'|\")',
                            rf'\1{info["filename"]}',
                            content
                        )
                        
                        # 2. 列表项：- CODE -> - FILENAME
                        content = re.sub(
                            rf'^(\s+)- {re.escape(code)}($)',
                            rf'\1- {info["filename"]}',
                            content,
                            flags=re.MULTILINE
                        )
                        
                        # 3. 嵌套格式：CODE/xxx -> FILENAME/xxx
                        content = re.sub(
                            rf'(\s+)- {re.escape(code)}/([a-zA-Z0-9_/]+)',
                            rf'\1- {info["filename"]}/\2',
                            content
                        )
                    
                    if content != original:
                        filepath.write_text(content, encoding='utf-8')
                        updated_count += 1
                        print(f"✓ {filepath.relative_to('.')}")
                
                except Exception as e:
                    print(f"✗ {filepath}: {e}")
    
    return updated_count

def main():
    os.chdir("/home/krvy/psydrugs.org")
    
    print("\n" + "=" * 70)
    print("药物文件名称中文化工具 - 第二阶段（修复引用）")
    print("=" * 70)
    
    # 获取完整映射
    print("\n[1/2] 读取完整映射...")
    mapping = get_all_mapping()
    print(f"✓ 找到 {len(mapping)} 个药物")
    
    # 显示预览
    remaining = {k: v for k, v in mapping.items() if v['filename'] != k}
    if remaining:
        print(f"\n还需要转换的英文代码：{len(remaining)} 个")
        for code, info in sorted(remaining.items())[:10]:
            print(f"  {code:12} -> {info['filename']}")
        if len(remaining) > 10:
            print(f"  ... 还有 {len(remaining) - 10} 个")
    
    # 修复引用
    print("\n[2/2] 修复所有引用...")
    fix_yaml_references(mapping)
    
    md_count = fix_markdown_references(mapping)
    print(f"✓ 共修复 {md_count} 个 Markdown 文件")
    
    print("\n" + "=" * 70)
    print("完成！")
    print("=" * 70)

if __name__ == "__main__":
    main()
