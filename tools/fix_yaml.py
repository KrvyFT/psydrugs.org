#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复YAML配置中的所有英文代码和不一致的引用
"""

import re
from pathlib import Path

def get_mapping():
    """获取英文代码到中文名的映射"""
    mapping = {}
    drugs_dir = Path("./source/drugs")
    
    for md_file in sorted(drugs_dir.glob("*.md")):
        if md_file.stem not in ["index", "compound", "introduction-to-overdose", "new-page"]:
            with open(md_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('title:'):
                        title = line.replace('title:', '').strip()
                        filename = title.replace('/', '_')
                        mapping[md_file.stem] = filename
                        break
    
    return mapping

def fix_yaml():
    """修复 YAML 文件中的所有引用"""
    yml_path = Path("./source/_data/wiki/drugs.yml")
    content = yml_path.read_text(encoding='utf-8')
    original = content
    
    mapping = get_mapping()
    
    # 按长度排序（长的先替换，避免短代码误匹配）
    sorted_codes = sorted(mapping.keys(), key=len, reverse=True)
    
    for code in sorted_codes:
        new_name = mapping[code]
        
        # 情况1：简单的列表项 - CODE
        content = re.sub(
            rf'^(\s+)- {re.escape(code)}$',
            rf'\1- {new_name}',
            content,
            flags=re.MULTILINE
        )
        
        # 情况2：嵌套路径 CODE/xxx
        content = re.sub(
            rf'^(\s+)- {re.escape(code)}/([a-zA-Z0-9_]+)$',
            rf'\1- {new_name}/\2',
            content,
            flags=re.MULTILINE
        )
    
    if content != original:
        yml_path.write_text(content, encoding='utf-8')
        print(f"✓ 修复 source/_data/wiki/drugs.yml")
        
        # 显示修改的行数
        orig_lines = original.split('\n')
        new_lines = content.split('\n')
        changed = sum(1 for o, n in zip(orig_lines, new_lines) if o != n)
        print(f"  共修改 {changed} 行")
        return True
    else:
        print("✗ YAML 文件没有需要修改的内容")
    return False

def main():
    import os
    os.chdir("/home/krvy/psydrugs.org")
    
    print("\n" + "=" * 70)
    print("修复 YAML 配置文件中的英文代码")
    print("=" * 70 + "\n")
    
    mapping = get_mapping()
    print(f"找到 {len(mapping)} 个药物映射")
    
    # 找出还有的英文代码
    yml_path = Path("./source/_data/wiki/drugs.yml")
    yml_content = yml_path.read_text(encoding='utf-8')
    
    # 提取所有 "- CODE" 格式的行
    pattern = r'^\s+- ([A-Z][A-Z0-9_/]*?)(?:/|$)'
    matches = re.findall(pattern, yml_content, re.MULTILINE)
    codes_in_yml = {m.split('/')[0] for m in matches}
    
    print(f"\nYAML 中现有的英文代码:")
    for code in sorted(codes_in_yml):
        if code in mapping:
            print(f"  {code:12} -> {mapping[code]}")
        else:
            print(f"  {code:12} (未找到映射)")
    
    fix_yaml()
    
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    main()
