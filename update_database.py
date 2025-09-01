#!/usr/bin/env python3
"""
更新数据库脚本 - 重新创建向量数据库以反映KerryZheng的故事
"""
import os
import shutil
from embed import create_db, qdrant_client, collection_name

def main():
    print("🔄 开始更新数据库...")
    
    try:
        # 关闭现有客户端连接
        print("📤 关闭现有数据库连接...")
        qdrant_client.close()
        
        # 删除旧数据库文件夹
        if os.path.exists("qdrant_db"):
            print("🗑️ 删除旧数据库...")
            shutil.rmtree("qdrant_db")
            print("✅ 旧数据库已删除")
        
        # 重新创建数据库
        print("🛠️ 重新创建数据库...")
        create_db()
        print("✅ 数据库更新完成！")
        
        print("\n🎉 KerryZheng的史莱姆故事已更新到向量数据库！")
        print("现在可以重新启动ChatBot来体验新的故事内容。")
        
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        print("请手动删除qdrant_db文件夹，然后重新运行程序。")

if __name__ == "__main__":
    main()
