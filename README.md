# SecuFlow Backend

SecuFlow 后端服务 - 基于 FastAPI 的 Git 数据挖掘与分析 API。

## 功能特性

- 🔍 Git 仓库数据挖掘和分析
- 📊 项目统计和可视化数据
- 🚀 基于 FastAPI 的高性能 RESTful API
- 💾 SQLite 数据存储
- 🔒 CORS 支持，可与前端无缝集成

## 本地开发

### 前置要求

- Python 3.9+
- Git

### 安装依赖

```shell
pip install -r requirements.txt
```

**注意**：如果使用 `python start.py` 启动，需要确保已安装 FastAPI：
```shell
pip install fastapi uvicorn[standard]
```

### Git Data Miner

使用 `process_git.py` 处理 Git 仓库数据并计算分析结果。

**用法:**

```shell
python process_git.py ~/test_repo/.git test_repo master
```

**参数说明:**

- `directory_path` - Git 仓库的 .git 目录路径
- `project_name` - 项目名称
- `project_branch` - Git 分支名

**可选参数:**

- `--db_url` - 数据库 URL (默认: sqlite:///miner_data.db)
- `-h, --help` - 显示帮助信息

### 启动开发服务器

#### 推荐方式（统一启动脚本）：
```shell
# 确保已安装依赖
pip install -r requirements.txt

# 从后端目录运行 - 自动检测环境并使用正确的方式启动
cd backend/
python start.py
```
- ✅ 本地开发：自动调用 `fastapi dev`（支持热重载）
- ✅ Docker 部署：直接使用 uvicorn
- ✅ 自动处理包导入和依赖问题

#### 手动 FastAPI CLI 方式：
```shell
# 从项目根目录运行
cd secuflow/back-end/
fastapi dev backend/main.py
```

服务器启动后访问:

服务器启动后访问:
- API 根路径: http://127.0.0.1:8000/
- 项目数据示例: http://127.0.0.1:8000/projects/1
- API 文档 (Swagger UI): http://127.0.0.1:8000/docs
- API 文档 (ReDoc): http://127.0.0.1:8000/redoc

## 生产部署

### 快速部署到 Render (推荐)

本项目已配置好 Render 部署文件，可以一键部署到 Render 免费层。

**部署步骤:**

1. 将代码推送到 GitHub
2. 在 [Render](https://render.com/) 注册账号
3. 创建新的 Web Service 并连接你的 GitHub 仓库
4. Render 会自动检测 `render.yaml` 配置并部署

详细部署指南请查看 [DEPLOYMENT.md](./DEPLOYMENT.md)

### Docker 部署

本项目包含 Dockerfile，可以使用 Docker 部署:

```shell
# 构建镜像
docker build -t secuflow-backend .

# 运行容器
docker run -p 8000:8000 secuflow-backend
```

## API 端点

主要 API 端点:

- `GET /` - 欢迎页面
- `GET /projects` - 项目列表
- `GET /projects/{project_id}` - 项目详情
- `GET /overview` - 总览数据

完整 API 文档请访问部署后的 `/docs` 路径。

## 环境变量

可选的环境变量配置:

- `DATABASE_URL` - 数据库连接 URL
- `PORT` - 服务器端口 (默认: 8000)
- `PYTHONUNBUFFERED` - Python 日志输出配置

## 技术栈

- **框架**: FastAPI
- **数据库**: SQLite + SQLAlchemy ORM
- **数据处理**: Pandas, NumPy
- **服务器**: Uvicorn
- **部署**: Docker + Render

## 项目结构

```
backend/
├── api/                  # API 路由
│   ├── overview.py      # 总览 API
│   ├── projects.py      # 项目列表 API
│   └── project_detail.py # 项目详情 API
├── main.py              # FastAPI 应用入口
├── database.py          # 数据库配置
├── process_git.py       # Git 数据处理脚本
├── requirements.txt     # Python 依赖
├── Dockerfile          # Docker 配置
├── render.yaml         # Render 部署配置
└── DEPLOYMENT.md       # 详细部署指南
```

## 开发说明

### 添加新的 API 端点

1. 在 `api/` 目录下创建新的路由文件
2. 在 `main.py` 中注册路由:

```python
from .api import your_new_router
app.include_router(your_new_router)
```

### 数据库迁移

如需修改数据库模型，可以使用 Alembic 进行迁移管理。

## 许可证

MIT License

## 支持

如有问题或建议，请提交 Issue 或 Pull Request。