#!/usr/bin/env python3
"""
自动生成或更新 drugs.yml，包含所有药物条目
"""
import os
from pathlib import Path

def scan_drugs():
    """扫描 drugs 目录，返回根目录条目和子目录条目。"""
    base = Path('/home/krvy/Psydrugs.icu/source/drugs')
    root_items = []
    folders = {}

    for entry in sorted(base.iterdir(), key=lambda p: p.name.lower()):
        # 根目录下的 md
        if entry.is_file() and entry.suffix == '.md':
            slug = entry.stem
            if slug not in {'index', 'introduction-to-overdose'}:
                # 排除模板
                if slug != 'new-page':
                    root_items.append(slug)
        # 子目录下的 md
        elif entry.is_dir():
            md_files = [p for p in entry.iterdir() if p.is_file() and p.suffix == '.md']
            if not md_files:
                continue
            folder_slug = entry.name
            slugs = []
            # 如果同名根文件存在，也允许手动保持，故直接加入
            for md in sorted(md_files, key=lambda p: p.name.lower()):
                slugs.append(f"{folder_slug}/{md.stem}")
            folders[folder_slug] = slugs

    return root_items, folders


def classify_drugs(root_items, folders):
    """将药物按类别分组。未匹配的放入“未分组”。"""
    # 扁平化子目录条目为 folder/slug
    all_items = set(root_items)
    for folder, slugs in folders.items():
        all_items.update(slugs)

    # 分类映射（可按需调整）
    categories = {
        '解离与麻醉': [
            'KTM', 'DXM', 'DXM/HTCT5THP', 'DXM/The_harm_of_dextromethorphan',
            'ATD', 'MMT', 'TTM', 'PPF'
        ],
        '阿片与镇痛': [
            'Opioids', 'CDI', 'DHCDI', 'DHCDI/OAR', 'MOP', 'PPD', 'DPX', 'TMD', 'PVR', 'NFP'
        ],
        '镇静催眠 / 睡眠': [
            'BZD', 'ZD', 'ZPC', 'ZPD', 'ZPO', 'CLH', 'DPH', 'THP', 'PMZ'
        ],
        '抗精神病 / 情绪稳定': [
            'ARP', 'ASP', 'QTP', 'OZP', 'RPD', 'VPA', 'LTG', 'PR', 'GBP'
        ],
        '抗抑郁与注意力': [
            'SRIs', 'TXT', 'BPP', 'RTL', 'AMs', 'CFI'
        ],
        '止吐 / 抗组胺 / 胃肠': [
            'AES', 'DPD', 'DMH', 'DPH', 'ACL', 'CLH', 'PCT', 'TAN', 'TEA'
        ],
        '补充剂与代谢调节': [
            'EI', 'SPM', 'MGT', 'MGT/OAR', 'TPL'
        ],
        '其他': [
            'compound', 'EtOH', 'BCF', 'PMZ', 'PCT', 'TPM'
        ],
    }

    grouped = {}
    used = set()
    for cate, items in categories.items():
        present = [x for x in items if x in all_items]
        if present:
            grouped[cate] = present
            used.update(present)

    # 未分组的放入“未分组”
    remaining = sorted(all_items - used)
    if remaining:
        grouped['未分组'] = remaining

    return grouped

def generate_drugs_yml():
    """生成新的 drugs.yml 内容，按自定义分类输出"""
    root_items, folders = scan_drugs()
    grouped = classify_drugs(root_items, folders)

    header = """name: 药物指南
title: 药物安全使用指南
subtitle: '科学用药 | 安全第一'
icon: /icons/medicine.png
cover: /icons/medicine.png
description: 常见药物的使用指南、注意事项及安全剂量说明
leftbar:
  - tree
  - recent
rightbar:
  - toc
comment_title: '如有问题或建议，欢迎在评论区交流讨论。'
comments:
  service: false
base_dir: /drugs/
tree:
  '导论':
    - introduction-to-overdose
    - /
    - index
"""

    # 分类输出
    for cate in grouped:
        header += f"  '{cate}':\n"
        for slug in grouped[cate]:
            header += f"    - {slug}\n"

    return header

def update_drugs_yml_file():
    """更新drugs.yml文件"""
    yml_path = '/home/krvy/Psydrugs.icu/source/_data/wiki/drugs.yml'
    new_content = generate_drugs_yml()
    root_items, folders = scan_drugs()
    grouped = classify_drugs(root_items, folders)
    total_items = sum(len(v) for v in grouped.values())
    
    # 备份原文件到项目根目录的 backups/，避免被 Hexo 当作数据文件解析
    if os.path.exists(yml_path):
        backup_dir = '/home/krvy/Psydrugs.icu/backups'
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, 'drugs.yml.backup')
        with open(yml_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)
        print(f"已备份原文件到: {backup_path}")
    
    # 写入新内容
    with open(yml_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ 已更新 {yml_path}")
    print(f"✓ 分类生成完成，合计 {total_items} 个条目")
    print(f"\n分类预览:")
    for cate in grouped:
        print(f"  {cate}: {len(grouped[cate])}")

if __name__ == '__main__':
    update_drugs_yml_file()
