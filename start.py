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
    # 本地开发环境：使用 FastAPI CLI（它会自动处理包导入和依赖）
    import subprocess
    import sys

    try:
        # 从项目根目录调用 FastAPI CLI，这样backend包能被正确识别
        os.chdir(parent_dir)  # 切换到项目根目录
        cmd = [sys.executable, "-m", "fastapi", "dev", "backend/main.py", "--host", "127.0.0.1", "--port", "8000"]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)
        sys.exit(0)

    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to start FastAPI dev server: {e}")
        print("Make sure you're in the correct directory and have FastAPI installed")
        sys.exit(1)
