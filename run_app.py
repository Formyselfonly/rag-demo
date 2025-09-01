#!/usr/bin/env python3
"""
史莱姆美食评论家 ChatBot 启动脚本
"""
import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """检查必要的依赖"""
    required_files = [
        "app.py",
        "embed.py", 
        "config.py",
        "data.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有必要文件已就绪")
    return True

def check_env_vars():
    """检查环境变量"""
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  警告: 未设置 OPENAI_API_KEY 环境变量")
        print("请确保在 .env 文件中设置了您的 OpenAI API Key")
        return False
    
    print("✅ 环境变量配置正常")
    return True

def main():
    print("🚀 启动史莱姆美食评论家 ChatBot...")
    print("=" * 50)
    
    # 检查文件
    if not check_requirements():
        sys.exit(1)
    
    # 检查环境变量
    check_env_vars()
    
    print("\n🌐 启动 Streamlit 应用...")
    print("📝 应用将在浏览器中自动打开")
    print("🔗 如果没有自动打开，请访问: http://localhost:8501")
    print("\n⏹️  按 Ctrl+C 停止应用")
    print("=" * 50)
    
    try:
        # 启动Streamlit应用
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 应用已停止，再见！")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
