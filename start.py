#!/usr/bin/env python3
"""
启动脚本 - 支持本地开发和Docker部署
"""
import sys
import os

# 获取目录信息
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 检测环境：检查是否在Docker中（所有文件在同一级目录）
is_docker = (os.path.exists(os.path.join(current_dir, 'main.py')) and
             os.path.exists(os.path.join(current_dir, 'database.py')) and
             os.path.exists(os.path.join(current_dir, 'api')))

if is_docker:
    # Docker环境：所有文件在同一级目录，使用绝对导入
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    os.environ.setdefault('PYTHONPATH', current_dir)

    try:
        # 绝对导入
        import database
        from api import overview_router, project_list_router, project_statistics_router
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware

        # 创建应用
        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.get("/")
        def read_root():
            return {"message": "Welcome to FastAPI with SQLite"}

        app.include_router(overview_router)
        app.include_router(project_list_router)
        app.include_router(project_statistics_router)

    except ImportError as e:
        print(f"Docker import error: {e}")
        sys.exit(1)

else:
    # 本地开发环境：backend是包结构
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    try:
        # 导入backend包
        import backend.main
        app = backend.main.app

    except ImportError as e:
        print(f"Local import error: {e}")
        sys.exit(1)

# 启动服务器
try:
    import uvicorn

    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
except Exception as e:
    print(f"Server error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
