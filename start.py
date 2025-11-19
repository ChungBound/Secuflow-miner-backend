#!/usr/bin/env python3
"""
启动脚本 - 正确处理包导入和应用启动
"""
import sys
import os

# 确保我们可以导入后端包
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 导入并运行应用
try:
    from main import app
    import uvicorn

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
    sys.exit(1)
