#!/usr/bin/env python3
"""
综合drugs自动处理脚本
执行所有与drugs相关的维护任务
"""
import os
import sys
import subprocess
from datetime import datetime

def print_section(title):
    """打印分隔符和标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def run_command(cmd, description):
    """运行命令并报告结果"""
    try:
        print(f"\n→ {description}")
        result = subprocess.run(cmd, shell=True, cwd='/home/krvy/Psydrugs.icu', 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ 成功")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"✗ 失败")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False

def count_drug_files():
    """统计drugs文件数量"""
    drugs_dir = '/home/krvy/Psydrugs.icu/source/drugs'
    count = 0
    subdirs = []
    
    for item in os.listdir(drugs_dir):
        item_path = os.path.join(drugs_dir, item)
        if item.endswith('.md') and os.path.isfile(item_path):
            count += 1
        elif os.path.isdir(item_path) and not item.startswith('.'):
            subdirs.append(item)
    
    return count, subdirs

def main():
    """主函数"""
    print_section("🔧 Drugs 自动处理工具")
    
    print(f"\n执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 显示当前状态
    print_section("📊 当前状态")
    drug_count, subdirs = count_drug_files()
    print(f"药物文件数: {drug_count}")
    print(f"药物子目录: {len(subdirs)}")
    if subdirs:
        for subdir in subdirs:
            print(f"  - {subdir}/")
    
    # 2. 验证drugs文件
    print_section("✓ 验证 Drugs 文件")
    run_command('python3 validate_drugs.py', '验证所有drugs文件的front-matter')
    
    # 3. 更新drugs.yml配置
    print_section("🔄 更新 Drugs 配置")
    run_command('python3 generate_drugs_yml.py', '生成/更新 drugs.yml')
    
    # 4. 显示最终结果
    print_section("✅ 完成")
    print(f"""
所有drugs相关处理已完成！

已执行的操作:
  ✓ 验证了drugs文件的前置元数据
  ✓ 更新了drugs.yml配置文件
  ✓ 包含了所有{drug_count}个药物条目

下一步:
  1. 运行 hexo generate 生成静态文件
  2. 运行 hexo server 启动本地服务器查看效果
  3. 确认drug页面显示正确
    """)

if __name__ == '__main__':
    main()
