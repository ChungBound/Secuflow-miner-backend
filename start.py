#!/usr/bin/env python3
"""
启动脚本 - 用于Docker部署
"""
import sys
import os

# 确保当前目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 设置PYTHONPATH环境变量
os.environ.setdefault('PYTHONPATH', current_dir)

# 导入并启动应用
try:
    import uvicorn
    from main import app

    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
