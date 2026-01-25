#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复剩余的短代码链接
"""

import os
import re
from pathlib import Path

# 额外的短代码映射
SHORT_CODE_MAPPING = {
    'SPM': 'supplements/补充剂',  # GABA 可能是补充剂相关
    'PR': 'antipsychotics/普瑞巴林',
    'TPL': 'supplements/茶碱',
    'TAN': 'supplements/茶氨酸',
    'EI': 'supplements/酶抑制剂',
    'THP': 'sedatives/苯海索',
    'MGT': 'supplements/苏糖酸镁',
    'GBP': 'antipsychotics/加巴喷丁',
    'RPD': 'antipsychotics/利培酮',
    'MMT': 'dissociatives/美金刚',
}

def fix_short_code_links_in_file(file_path):
    """修复单个文件中的短代码链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 匹配所有 /drugs/xxx 格式的链接，其中 xxx 是短代码
        pattern = r'\[([^\]]+)\]\(/drugs/([A-Z]{2,5})(/[^)]*)?(\))'
        
        def replace_link(match):
            nonlocal modified
            link_text = match.group(1)
            short_code = match.group(2)
            suffix = match.group(3) or ''
            closing = match.group(4)
            
            # 查找对应的新路径
            if short_code in SHORT_CODE_MAPPING:
                new_path = SHORT_CODE_MAPPING[short_code]
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
    
    # 遍历所有 .md 文件
    for file_path in source_dir.glob('**/*.md'):
        was_modified, path = fix_short_code_links_in_file(file_path)
        if was_modified:
            modified_files.append(path)
    
    print(f"\n修复完成！共修改了 {len(modified_files)} 个文件：")
    for file in modified_files:
        print(f"  - {file}")

if __name__ == '__main__':
    main()
