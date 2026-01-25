#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 drugs 文件夹分类后的所有链接引用
"""

import os
import re
from pathlib import Path

# 定义药物文件的新路径映射
DRUG_PATH_MAPPING = {
    # 阿片类 - opioids
    '阿片类药物': 'opioids/阿片类药物',
    'Opioids': 'opioids/阿片类药物',
    'CDI': 'opioids/可待因',
    '可待因': 'opioids/可待因',
    'DHCDI': 'opioids/二氢可待因',
    '二氢可待因': 'opioids/二氢可待因',
    'MOP': 'opioids/吗啡',
    '吗啡': 'opioids/吗啡',
    'PPD': 'opioids/杜冷丁',
    '杜冷丁': 'opioids/杜冷丁',
    'TMD': 'opioids/曲马多',
    '曲马多': 'opioids/曲马多',
    'DPX': 'opioids/地芬诺酯',
    '地芬诺酯': 'opioids/地芬诺酯',
    '喷托维林': 'opioids/喷托维林',
    '奈福泮': 'opioids/奈福泮',
    
    # 解离类 - dissociatives
    'DXM': 'dissociatives/右美沙芬_愈美片',
    '右美沙芬': 'dissociatives/右美沙芬_愈美片',
    '右美沙芬_愈美片': 'dissociatives/右美沙芬_愈美片',
    '氯胺酮': 'dissociatives/氯胺酮',
    'ATD': 'dissociatives/金刚烷胺',
    '金刚烷胺': 'dissociatives/金刚烷胺',
    'MMT': 'dissociatives/美金刚',
    '美金刚': 'dissociatives/美金刚',
    '替来他明': 'dissociatives/替来他明',
    '丙泊酚': 'dissociatives/丙泊酚',
    'DPD': 'dissociatives/地芬尼多',
    '地芬尼多': 'dissociatives/地芬尼多',
    
    # 镇静催眠类 - sedatives
    'BZD': 'sedatives/苯二氮卓类药物',
    '苯二氮卓类': 'sedatives/苯二氮卓类药物',
    '苯二氮卓类药物': 'sedatives/苯二氮卓类药物',
    'Z药物': 'sedatives/Z药物',
    '佐匹克隆': 'sedatives/佐匹克隆',
    'ZPD': 'sedatives/唑吡坦',
    '唑吡坦': 'sedatives/唑吡坦',
    '扎来普隆': 'sedatives/扎来普隆',
    'CLH': 'sedatives/水合氯醛',
    '水合氯醛': 'sedatives/水合氯醛',
    'DPH': 'sedatives/苯海拉明',
    '苯海拉明': 'sedatives/苯海拉明',
    '苯海索': 'sedatives/苯海索',
    '异丙嗪': 'sedatives/异丙嗪',
    
    # 抗精神病类 - antipsychotics
    'QTP': 'antipsychotics/喹硫平',
    '喹硫平': 'antipsychotics/喹硫平',
    '奥氮平': 'antipsychotics/奥氮平',
    '利培酮': 'antipsychotics/利培酮',
    'ARP': 'antipsychotics/阿立哌唑',
    '阿立哌唑': 'antipsychotics/阿立哌唑',
    'ASP': 'antipsychotics/氨磺必利',
    '氨磺必利': 'antipsychotics/氨磺必利',
    '丙戊酸': 'antipsychotics/丙戊酸',
    '拉莫三嗪': 'antipsychotics/拉莫三嗪',
    '普瑞巴林': 'antipsychotics/普瑞巴林',
    '加巴喷丁': 'antipsychotics/加巴喷丁',
    
    # 抗抑郁类 - antidepressants
    'SRIs': 'antidepressants/血清素再摄取抑制剂',
    '血清素再摄取抑制剂': 'antidepressants/血清素再摄取抑制剂',
    '托莫西汀': 'antidepressants/托莫西汀',
    'BPP': 'antidepressants/安非他酮',
    '安非他酮': 'antidepressants/安非他酮',
    '哌醋甲酯': 'antidepressants/哌醋甲酯',
    'AMs': 'antidepressants/苯丙胺类药物',
    '苯丙胺类药物': 'antidepressants/苯丙胺类药物',
    'CFI': 'antidepressants/咖啡因',
    '咖啡因': 'antidepressants/咖啡因',
    'ADD': 'antidepressants/烷胺类药物',
    '烷胺类药物': 'antidepressants/烷胺类药物',
    
    # 止吐/抗组胺类 - antiemetics
    'AES': 'antiemetics/止吐药',
    '止吐药': 'antiemetics/止吐药',
    'DMH': 'antiemetics/茶苯海明',
    '茶苯海明': 'antiemetics/茶苯海明',
    'ACL': 'antiemetics/槟榔碱',
    '槟榔碱': 'antiemetics/槟榔碱',
    '吡拉西坦': 'antiemetics/吡拉西坦',
    
    # 补充剂类 - supplements
    '酶抑制剂': 'supplements/酶抑制剂',
    '补充剂': 'supplements/补充剂',
    '苏糖酸镁': 'supplements/苏糖酸镁',
    '茶碱': 'supplements/茶碱',
    'TAN': 'supplements/茶氨酸',
    '茶氨酸': 'supplements/茶氨酸',
    '茶': 'supplements/茶',
    
    # 其他类 - others
    'compound': 'others/compound',
    '复方': 'others/compound',
    '复方专题': 'others/compound',
    'EtOH': 'others/乙醇',
    '乙醇': 'others/乙醇',
    '酒': 'others/乙醇',
    'BCF': 'others/巴氯芬',
    '巴氯芬': 'others/巴氯芬',
    'TPM': 'others/TPM',
    'Cigarette': 'others/Cigarette',
    '香烟': 'others/Cigarette',
    'psychedelics': 'others/psychedelics',
    'introduction-to-overdose': 'others/introduction-to-overdose',
    'new-page': 'others/new-page',
}

def fix_drug_links_in_file(file_path):
    """修复单个文件中的药物链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 匹配所有 /drugs/xxx 或 /Drugs/xxx 格式的链接
        pattern = r'\[([^\]]+)\]\(/[Dd]rugs/([^/)]+)(/[^)]*)?(\))'
        
        def replace_link(match):
            nonlocal modified
            link_text = match.group(1)
            drug_name = match.group(2)
            suffix = match.group(3) or ''
            closing = match.group(4)
            
            # 查找对应的新路径
            if drug_name in DRUG_PATH_MAPPING:
                new_path = DRUG_PATH_MAPPING[drug_name]
                modified = True
                return f'[{link_text}](/drugs/{new_path}{suffix}{closing}'
            else:
                # 保持原样
                return match.group(0)
        
        content = re.sub(pattern, replace_link, content)
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, file_path
        return False, None
        
    except Exception as e:
        print(f"处理文件时出错 {file_path}: {e}")
        return False, None

def main():
    """主函数"""
    source_dir = Path('/home/krvy/psydrugs.org/source')
    
    modified_files = []
    
    # 遍历所有 .md 和 .html 文件
    for ext in ['**/*.md', '**/*.html']:
        for file_path in source_dir.glob(ext):
            was_modified, path = fix_drug_links_in_file(file_path)
            if was_modified:
                modified_files.append(path)
    
    print(f"\n修复完成！共修改了 {len(modified_files)} 个文件：")
    for file in modified_files:
        print(f"  - {file}")

if __name__ == '__main__':
    main()
