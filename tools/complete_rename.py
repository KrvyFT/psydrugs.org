#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的药物文件重命名和引用修正脚本
处理含有特殊字符的文件名
"""

import os
import re
import shutil
from pathlib import Path
from collections import defaultdict

def sanitize_filename(title):
    """将标题转换为有效的文件名（处理特殊字符）"""
    # 将斜杠替换为下划线
    filename = title.replace('/', '_')
    # 移除其他可能不安全的字符
    filename = re.sub(r'[<>:"|?*]', '', filename)
    return filename

def get_drug_mapping():
    """获取所有药物文件的编码->中文名映射"""
    mapping = {}
    drugs_dir = Path("./source/drugs")
    
    for md_file in sorted(drugs_dir.glob("*.md")):
        if md_file.stem not in ["index", "compound", "introduction-to-overdose", "new-page"]:
            with open(md_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('title:'):
                        title = line.replace('title:', '').strip()
                        mapping[md_file.stem] = {
                            'title': title,
                            'filename': sanitize_filename(title)
                        }
                        break
    
    return mapping

def rename_files(mapping):
    """重命名所有药物文件"""
    drugs_dir = Path("./source/drugs")
    renamed_count = 0
    
    for code, info in mapping.items():
        old_path = drugs_dir / f"{code}.md"
        new_path = drugs_dir / f"{info['filename']}.md"
        
        if old_path.exists():
            if not new_path.exists():
                old_path.rename(new_path)
                print(f"✓ {code:12} -> {info['filename']}")
                renamed_count += 1
            else:
                print(f"⚠ {info['filename']}.md 已存在，跳过 {code}")
        else:
            print(f"✗ 未找到 {code}.md")
    
    return renamed_count

def update_drugs_yml(mapping):
    """更新 source/_data/wiki/drugs.yml"""
    yml_path = Path("./source/_data/wiki/drugs.yml")
    
    if not yml_path.exists():
        print(f"⚠ {yml_path} 不存在")
        return False
    
    content = yml_path.read_text(encoding='utf-8')
    original = content
    
    # 替换树结构中的代码引用
    for code, info in mapping.items():
        # 匹配各种缩进和格式的列表项
        content = re.sub(
            rf'(\s+)- {re.escape(code)}($|\n)',
            rf'\1- {info["filename"]}\n',
            content
        )
    
    if content != original:
        yml_path.write_text(content, encoding='utf-8')
        print(f"✓ 更新 source/_data/wiki/drugs.yml")
        return True
    return False

def update_markdown_files(mapping):
    """更新所有 markdown 文件中的链接"""
    updated_count = 0
    
    for root, dirs, files in os.walk("./source"):
        # 跳过某些目录
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '.hexo_asset_dir']]
        
        for file in files:
            if file.endswith('.md'):
                filepath = Path(root) / file
                
                try:
                    content = filepath.read_text(encoding='utf-8')
                    original = content
                    
                    for code, info in mapping.items():
                        # 替换 Markdown 链接中的代码
                        # [text](/drugs/CODE) -> [text](/drugs/FILENAME)
                        content = re.sub(
                            rf'(/drugs/){re.escape(code)}(?=/|\'|\"|\s|$|\])',
                            rf'\1{info["filename"]}',
                            content
                        )
                        
                        # 替换列表项中的代码引用（带缩进）
                        content = re.sub(
                            rf'^(\s+)- {re.escape(code)}($|\n)',
                            rf'\1- {info["filename"]}\n',
                            content,
                            flags=re.MULTILINE
                        )
                        
                        # 替换 CODE/xxx 格式的嵌套引用
                        content = re.sub(
                            rf'(\s+- ){re.escape(code)}/([a-zA-Z0-9_/]+)',
                            rf'\1{info["filename"]}/\2',
                            content
                        )
                    
                    if content != original:
                        filepath.write_text(content, encoding='utf-8')
                        updated_count += 1
                        print(f"✓ 更新 {filepath.relative_to('.')}")
                
                except Exception as e:
                    print(f"✗ 错误处理 {filepath}: {e}")
    
    return updated_count

def update_html_files(mapping):
    """更新 HTML 文件中的链接"""
    updated_count = 0
    
    for root, dirs, files in os.walk("./source"):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules']]
        
        for file in files:
            if file.endswith('.html'):
                filepath = Path(root) / file
                
                try:
                    content = filepath.read_text(encoding='utf-8')
                    original = content
                    
                    for code, info in mapping.items():
                        # 替换 HTML 中的链接
                        content = re.sub(
                            rf'(/drugs/){re.escape(code)}(?=/|\'|\"|\s|>)',
                            rf'\1{info["filename"]}',
                            content
                        )
                    
                    if content != original:
                        filepath.write_text(content, encoding='utf-8')
                        updated_count += 1
                        print(f"✓ 更新 {filepath.relative_to('.')}")
                
                except Exception as e:
                    print(f"✗ 错误处理 {filepath}: {e}")
    
    return updated_count

def handle_subdirectories(mapping):
    """处理药物的子目录（如 DXM/、MGT/）"""
    drugs_dir = Path("./source/drugs")
    updated_count = 0
    
    for code, info in mapping.items():
        old_dir = drugs_dir / code
        new_dir = drugs_dir / info['filename']
        
        if old_dir.exists() and old_dir.is_dir():
            if not new_dir.exists():
                old_dir.rename(new_dir)
                print(f"✓ 重命名目录 {code}/ -> {info['filename']}/")
                updated_count += 1
            else:
                print(f"⚠ 目录 {info['filename']}/ 已存在，跳过 {code}/")
    
    return updated_count

def main():
    os.chdir("/home/krvy/psydrugs.org")
    
    print("\n" + "=" * 70)
    print("药物文件名称中文化工具 - 完整执行")
    print("=" * 70)
    
    # 第一步：获取映射
    print("\n[1/6] 读取药物文件映射...")
    mapping = get_drug_mapping()
    print(f"✓ 找到 {len(mapping)} 个药物文件")
    
    # 显示映射预览
    print("\n映射预览：")
    for i, (code, info) in enumerate(sorted(mapping.items())[:8]):
        print(f"  {code:12} -> {info['filename']}")
    if len(mapping) > 8:
        print(f"  ... 还有 {len(mapping) - 8} 个")
    
    # 第二步：重命名文件
    print("\n[2/6] 重命名药物文件...")
    renamed = rename_files(mapping)
    print(f"✓ 共重命名 {renamed} 个文件")
    
    # 第三步：处理子目录
    print("\n[3/6] 重命名药物子目录...")
    renamed_dirs = handle_subdirectories(mapping)
    print(f"✓ 共重命名 {renamed_dirs} 个目录")
    
    # 第四步：更新 YAML 配置
    print("\n[4/6] 更新 YAML 配置文件...")
    update_drugs_yml(mapping)
    
    # 第五步：更新 Markdown 文件引用
    print("\n[5/6] 更新 Markdown 文件中的引用...")
    md_updated = update_markdown_files(mapping)
    print(f"✓ 共更新 {md_updated} 个 Markdown 文件")
    
    # 第六步：更新 HTML 文件引用
    print("\n[6/6] 更新 HTML 文件中的引用...")
    html_updated = update_html_files(mapping)
    print(f"✓ 共更新 {html_updated} 个 HTML 文件")
    
    print("\n" + "=" * 70)
    print("完成！")
    print("=" * 70)
    print("\n后续步骤：")
    print("1. 运行命令重新生成网站：")
    print("   hexo clean && hexo g")
    print("\n2. 测试网站：")
    print("   hexo s")
    print("\n3. 如果一切正常，提交更改：")
    print("   git add -A && git commit -m '药物文件名中文化'")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
