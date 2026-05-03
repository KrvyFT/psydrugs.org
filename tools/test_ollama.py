#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama API 连接测试脚本
"""

import requests
import json
import sys

def test_ollama_connection(host="http://127.0.0.1:443", model="deepseek"):
    """测试 Ollama API 连接"""
    url = f"{host}/api/generate"

    payload = {
        "model": model,
        "prompt": "Hello, please respond with a simple greeting.",
        "stream": False
    }

    try:
        print(f"正在测试连接：{url}")
        print(f"使用模型：{model}")
        print("-" * 50)

        response = requests.post(url, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            print("✅ 连接成功！")
            print(f"响应：{result.get('response', '无响应内容')}")
            return True
        else:
            print(f"❌ HTTP 错误：{response.status_code}")
            print(f"响应：{response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ 连接失败：无法连接到服务器")
        print("请检查：")
        print("1. Ollama 是否已启动")
        print("2. 端口是否正确（443）")
        print("3. 防火墙设置")
        return False
    except requests.exceptions.Timeout:
        print("❌ 连接超时：服务器响应太慢")
        return False
    except Exception as e:
        print(f"❌ 其他错误：{e}")
        return False

def main():
    print("Ollama API 连接测试工具")
    print("=" * 50)

    # 测试本地连接
    print("\n[1/2] 测试本地连接 (127.0.0.1:443)...")
    local_success = test_ollama_connection("http://127.0.0.1:443")

    # 测试公网连接
    print("\n[2/2] 测试公网连接 (frp-bar.com:56559)...")
    public_success = test_ollama_connection("https://frp-bar.com:56559")

    print("\n" + "=" * 50)
    print("测试结果：")

    if local_success:
        print("✅ 本地连接正常")
    else:
        print("❌ 本地连接失败")

    if public_success:
        print("✅ 公网连接正常")
    else:
        print("❌ 公网连接失败")

    if local_success or public_success:
        print("\n🎉 至少一个连接正常，可以使用搜索功能！")
    else:
        print("\n❌ 所有连接都失败，请检查 Ollama 配置")
        sys.exit(1)

if __name__ == "__main__":
    main()
