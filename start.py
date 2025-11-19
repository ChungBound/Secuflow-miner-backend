#!/usr/bin/env python3
"""
启动脚本 - 支持本地开发和Docker部署
"""
import sys
import os

# 获取目录信息
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 检测环境：检查是否在Docker容器中
# Docker容器会有特定的环境变量或文件结构
is_docker = (
    # 检查Docker环境变量
    os.path.exists('/.dockerenv') or
    os.environ.get('DOCKER_CONTAINER') == 'true' or
    # 检查是否所有文件都在当前目录且没有上级backend包结构
    (os.path.exists(os.path.join(current_dir, 'main.py')) and
     os.path.exists(os.path.join(current_dir, 'database.py')) and
     os.path.exists(os.path.join(current_dir, 'api')) and
     not os.path.exists(os.path.join(parent_dir, 'backend')))
)

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

        # 优先使用有FastAPI的Python环境
        python_cmds = [
            # 首先尝试conda环境（通常有包）
            ["/Users/zzb/anaconda3/bin/python", "-m", "fastapi", "dev", "backend/main.py", "--host", "127.0.0.1", "--port", "8000"],
            ["/Users/zzb/anaconda3/bin/python3", "-m", "fastapi", "dev", "backend/main.py", "--host", "127.0.0.1", "--port", "8000"],
            # 然后尝试当前Python环境
            [sys.executable, "-m", "fastapi", "dev", "backend/main.py", "--host", "127.0.0.1", "--port", "8000"],
            # 最后尝试系统Python
            ["/usr/bin/python3", "-m", "fastapi", "dev", "backend/main.py", "--host", "127.0.0.1", "--port", "8000"],
            ["python3", "-m", "fastapi", "dev", "backend/main.py", "--host", "127.0.0.1", "--port", "8000"]
        ]

        for cmd in python_cmds:
            try:
                print(f"Trying: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=False)
                if result.returncode == 0:
                    sys.exit(0)
                break
            except FileNotFoundError:
                continue
        else:
            print("Error: Could not find Python with FastAPI installed")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to start FastAPI dev server: {e}")
        print("Make sure you're in the correct directory and have FastAPI installed")
        sys.exit(1)

# 注意：启动逻辑在上面的 if/else 分支中处理
# Docker环境直接运行应用，本地环境调用FastAPI CLI
