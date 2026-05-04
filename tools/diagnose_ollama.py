#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama 启动诊断工具
"""

import subprocess
import sys
import time

def run_command(cmd, timeout=5):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "命令执行超时"
    except Exception as e:
        return -1, "", str(e)

def check_ollama_installed():
    """检查 Ollama 是否已安装"""
    print("[1/6] 检查 Ollama 是否已安装...")
    code, stdout, stderr = run_command("ollama --version")
    if code == 0:
        print(f"✅ Ollama 已安装：{stdout}")
        return True
    else:
        print("❌ Ollama 未找到，请确保已安装")
        return False

def check_deepseek_model():
    """检查 deepseek 模型是否已下载"""
    print("\n[2/6] 检查 deepseek 模型...")
    code, stdout, stderr = run_command("ollama list")
    if code == 0:
        if "deepseek" in stdout:
            print("✅ deepseek 模型已下载")
            print(f"模型列表：\n{stdout}")
            return True
        else:
            print("❌ deepseek 模型未找到")
            print(f"已安装的模型：\n{stdout}")
            print("\n建议：运行 'ollama pull deepseek' 下载模型")
            return False
    else:
        print(f"❌ 检查失败：{stderr}")
        return False

def check_port_availability():
    """检查 443 端口是否被占用"""
    print("\n[3/6] 检查端口 443...")
    code, stdout, stderr = run_command("netstat -ano | findstr :443")
    if code == 0 and stdout:
        print(f"⚠️  端口 443 已被占用：\n{stdout}")
        print("\n建议：")
        print("1. 改用其他端口，例如 11434（Ollama 默认）")
        print("2. 或结束占用端口的进程")
        return False
    else:
        print("✅ 端口 443 可用")
        return True

def check_ollama_running():
    """检查 Ollama 是否正在运行"""
    print("\n[4/6] 检查 Ollama 服务是否运行...")
    code, stdout, stderr = run_command("ollama ps")
    if code == 0:
        if stdout:
            print("✅ Ollama 正在运行")
            print(f"运行中的模型：\n{stdout}")
            return True
        else:
            print("ℹ️  Ollama 已安装但未运行")
            return False
    else:
        print(f"❌ 检查失败：{stderr}")
        return False

def recommend_solution():
    """根据诊断结果给出建议"""
    print("\n[5/6] 诊断完成，给出解决方案...")
    
    # 重新运行诊断
    ollama_ok = check_ollama_installed()
    if not ollama_ok:
        return
    
    deepseek_ok = check_deepseek_model()
    port_ok = check_port_availability()
    running_ok = check_ollama_running()
    
    print("\n" + "="*60)
    print("解决方案：")
    print("="*60)
    
    if not deepseek_ok:
        print("\n1️⃣  首先下载 deepseek 模型：")
        print("   ollama pull deepseek")
    
    if not port_ok:
        print("\n2️⃣  修改启动脚本使用默认端口 11434：")
        print("   编辑 tools/start_ollama.bat 或 start_ollama.ps1")
        print("   将 OLLAMA_HOST 改为 127.0.0.1:11434")
        print("   同时更新 source/js/deepseek-search.js 中的 defaultApiHost")
    else:
        print("\n2️⃣  启动 Ollama 服务：")
        print("   方式 A - 双击运行：tools\\start_ollama.bat")
        print("   方式 B - PowerShell 运行：.\\tools\\start_ollama.ps1")
        print("   方式 C - 命令行运行：")
        print("       $env:OLLAMA_HOST = '127.0.0.1:443'")
        print("       $env:OLLAMA_ORIGINS = '*'")
        print("       ollama serve")
    
    if running_ok:
        print("\n✅ 所有检查通过，Ollama 已准备就绪！")
    
    print("\n3️⃣  启动后测试：")
    print("   python tools/test_ollama.py")

def main():
    print("="*60)
    print("Ollama 启动诊断工具")
    print("="*60)
    
    check_ollama_installed()
    check_deepseek_model()
    check_port_availability()
    check_ollama_running()
    recommend_solution()
    
    print("\n" + "="*60)
    print("诊断完成")
    print("="*60)

if __name__ == "__main__":
    main()
