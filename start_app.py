#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动脚本，用于在IDE中直接运行Flask应用
"""

import os
import subprocess
import sys

def main():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置虚拟环境路径
    venv_path = os.path.join(current_dir, 'venv')
    python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')
    
    # 检查虚拟环境是否存在
    if not os.path.exists(python_exe):
        print("错误: 找不到虚拟环境，请先创建虚拟环境:")
        print("python -m venv venv")
        return 1
    
    # 设置app.py路径
    app_path = os.path.join(current_dir, 'app.py')
    
    # 检查app.py是否存在
    if not os.path.exists(app_path):
        print("错误: 找不到app.py文件")
        return 1
    
    # 在虚拟环境中运行app.py
    print("正在虚拟环境中启动Flask应用...")
    try:
        # 使用虚拟环境中的Python解释器运行app.py
        result = subprocess.run([python_exe, 'app.py'], cwd=current_dir)
        return result.returncode
    except Exception as e:
        print(f"启动应用时出错: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())