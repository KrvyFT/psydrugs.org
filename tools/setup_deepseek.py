#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deepseek AI 搜索集成工具
用于配置和测试 Deepseek API 集成

使用方法：
    python tools/setup_deepseek.py --api-key YOUR_KEY [--api-host CUSTOM_HOST]
"""

import argparse
import json
import re
from pathlib import Path


def update_search_page_config(api_key: str, api_host: str = None) -> None:
    """更新搜索页面中的 API key"""
    search_page = Path("./source/search/index.md")
    if not search_page.exists():
        print(f"✗ 搜索页面不存在：{search_page}")
        return

    content = search_page.read_text(encoding='utf-8')
    
    # 替换 API key
    if api_key:
        content = re.sub(
            r'data-api-key="[^"]*"',
            f'data-api-key="{api_key}"',
            content
        )
    
    # 如果提供了自定义 API host，也替换
    if api_host:
        # 在脚本标签后面添加自定义 host
        if 'data-api-host' not in content:
            content = re.sub(
                r'(<script src="/js/deepseek-search.js".*?)(\s*>)',
                rf'\1 data-api-host="{api_host}"\2',
                content
            )
        else:
            content = re.sub(
                r'data-api-host="[^"]*"',
                f'data-api-host="{api_host}"',
                content
            )
    
    search_page.write_text(content, encoding='utf-8')
    print(f"✓ 搜索页面已更新：{search_page}")


def update_js_script(api_host: str = None) -> None:
    """如需要，更新 JS 脚本中的 API host 配置"""
    script_path = Path("./source/js/deepseek-search.js")
    if not script_path.exists():
        print(f"✗ 脚本不存在：{script_path}")
        return

    if api_host:
        content = script_path.read_text(encoding='utf-8')
        content = re.sub(
            r"const defaultApiHost = '[^']*'",
            f"const defaultApiHost = '{api_host}'",
            content
        )
        script_path.write_text(content, encoding='utf-8')
        print(f"✓ JS 脚本已更新默认 API Host")


def create_config_template() -> None:
    """创建配置文件模板"""
    config_path = Path("./tools/deepseek_config.json")
    template = {
        "api_key": "YOUR_DEEPSEEK_API_KEY",
        "api_host": "https://api.deepseek.ai/v1/search",
        "repository": "psydrugs.org",
        "enabled": False,
        "description": "Deepseek AI 搜索配置文件"
    }
    config_path.write_text(json.dumps(template, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✓ 配置模板已创建：{config_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description='Deepseek AI 搜索集成工具')
    parser.add_argument('--api-key', help='Deepseek API Key', required=False)
    parser.add_argument('--api-host', help='自定义 API 地址（可选）', required=False)
    parser.add_argument('--init', action='store_true', help='初始化配置文件')
    
    args = parser.parse_args()

    if args.init:
        create_config_template()
        return

    if args.api_key:
        update_search_page_config(args.api_key, args.api_host)
        if args.api_host:
            update_js_script(args.api_host)
        print("\n[✓] 配置完成！")
        print("   - 搜索页面：http://localhost:4000/search/")
        print("   - API Key 已安全应用到搜索页面")
        if args.api_host:
            print(f"   - 自定义 API 地址：{args.api_host}")
    else:
        print("请提供 --api-key 参数")
        parser.print_help()


if __name__ == '__main__':
    main()
