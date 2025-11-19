# SecuFlow 后端部署指南

本文档详细介绍如何将 SecuFlow 后端服务部署到 Render 平台（免费方案）。

## 为什么选择 Render？

- ✅ 完全免费的 Web Service 层级
- ✅ 原生支持 Dockerfile 部署
- ✅ 自动提供 HTTPS 和自定义域名
- ✅ 与 Vercel 前端配合使用非常流行
- ✅ 配置简单，部署快速
- ⚠️ 免费层会在 15 分钟不活动后休眠（首次请求会自动唤醒，约需 30-60 秒）

## 部署前准备

### 1. 确保代码已推送到 GitHub

将你的代码推送到 GitHub 仓库（Render 支持 GitHub、GitLab 和 Bitbucket）。

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. 注册 Render 账号

1. 访问 [Render 官网](https://render.com/)
2. 点击右上角 **Sign Up** 注册账号
3. 推荐使用 **GitHub 账号** 直接登录，这样可以更方便地连接仓库

## 部署步骤

### 步骤 1：创建新的 Web Service

1. 登录 Render 后，点击 **Dashboard**
2. 点击右上角的 **New +** 按钮
3. 选择 **Web Service**

### 步骤 2：连接 GitHub 仓库

1. 选择 **Connect a repository**
2. 如果首次使用，需要授权 Render 访问你的 GitHub 账号
3. 找到并选择你的后端项目仓库（`secuFlow/back-end/backend` 或类似路径）
4. 点击 **Connect**

### 步骤 3：配置 Web Service

Render 会自动检测到 `render.yaml` 配置文件，但你也可以手动配置：

#### 基本配置

- **Name**: `secuflow-backend`（或自定义名称）
- **Region**: 选择 `Oregon (US West)` 或离你用户最近的区域
- **Branch**: `main`（或你的主分支名称）
- **Root Directory**: 如果你的后端代码在子目录，需要指定路径，例如 `backend`

#### 构建配置

- **Runtime**: 选择 **Docker**
- **Dockerfile Path**: `./Dockerfile`

#### 服务配置

- **Plan**: 选择 **Free**
- **Environment Variables**: 通常不需要额外配置，系统会自动设置

### 步骤 4：部署

1. 检查所有配置无误后，点击页面底部的 **Create Web Service** 按钮
2. Render 会开始自动构建和部署你的应用
3. 构建过程大约需要 3-5 分钟，你可以在控制台看到实时日志

### 步骤 5：查看部署状态

部署完成后：

1. 你会在页面顶部看到应用的 URL，格式类似：`https://secuflow-backend.onrender.com`
2. 状态显示为 **Live** 表示部署成功
3. 点击 URL 或访问 `https://your-app.onrender.com/` 应该能看到：
   ```json
   {"message": "Welcome to FastAPI with SQLite"}
   ```

### 步骤 6：测试 API 端点

测试几个关键端点确保服务正常运行：

```bash
# 测试根路径
curl https://your-app.onrender.com/

# 测试项目列表（如果数据库中有数据）
curl https://your-app.onrender.com/projects/1
```

## 前端配置

### 在 Vercel 前端项目中配置后端 API 地址

#### 方法 1：通过 Vercel Dashboard 配置

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择你的前端项目
3. 进入 **Settings** → **Environment Variables**
4. 添加新的环境变量：
   - **Name**: `VITE_API_BASE_URL` 或 `NEXT_PUBLIC_API_URL`（根据你的框架）
   - **Value**: `https://your-app.onrender.com`
   - **Environments**: 选择 `Production`、`Preview`、`Development`
5. 点击 **Save**
6. 重新部署前端项目以使环境变量生效

#### 方法 2：通过 vercel.json 配置

在前端项目根目录创建或编辑 `vercel.json`：

```json
{
  "env": {
    "VITE_API_BASE_URL": "https://your-app.onrender.com"
  }
}
```

#### 在前端代码中使用

```javascript
// React + Vite
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Next.js
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 使用示例
fetch(`${API_BASE_URL}/projects/1`)
  .then(response => response.json())
  .then(data => console.log(data));
```

## 自动部署

配置完成后，每次你推送代码到 GitHub 的指定分支，Render 会自动检测并重新部署应用。

### 查看部署历史

在 Render Dashboard 的服务页面，你可以：
- 查看所有部署历史
- 查看每次部署的日志
- 回滚到之前的版本

## CORS 配置

你的代码中已经配置了 CORS，允许所有来源：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

如果需要更严格的安全配置，可以修改 `allow_origins` 为你的前端域名：

```python
allow_origins=["https://your-frontend.vercel.app"],
```

## 常见问题

### Q1: 部署后首次访问很慢？

**A**: 这是正常现象。Render 免费层在 15 分钟不活动后会休眠，首次请求需要 30-60 秒唤醒服务。之后的请求会很快。

**解决方案**：
- 使用付费方案（$7/月起）避免休眠
- 使用定时任务每隔 10-14 分钟 ping 一次服务保持活跃
- 在前端添加加载提示，告知用户首次加载可能较慢

### Q2: 数据库数据会丢失吗？

**A**: 是的。免费层不提供持久化存储，服务重启后 SQLite 数据会丢失。

**解决方案**：
- 对于测试/演示项目，可以在应用启动时初始化示例数据
- 生产环境建议使用云数据库（PostgreSQL、MySQL 等）
- Render 付费方案提供持久化磁盘存储

### Q3: 如何查看应用日志？

**A**: 在 Render Dashboard 的服务页面，点击 **Logs** 标签可以查看实时日志和历史日志。

### Q4: 部署失败怎么办？

**A**: 检查以下几点：
1. 确认 Dockerfile 路径正确
2. 查看构建日志，找到具体错误信息
3. 确认 requirements.txt 中的依赖都能正常安装
4. 检查代码中是否有硬编码的本地路径

### Q5: 如何绑定自定义域名？

**A**: 
1. 在 Render Dashboard 的服务页面，点击 **Settings**
2. 找到 **Custom Domain** 部分
3. 添加你的域名并按照提示配置 DNS 记录
4. Render 会自动配置 HTTPS 证书

### Q6: 如何更新环境变量？

**A**:
1. 在 Render Dashboard 的服务页面，点击 **Environment**
2. 添加或修改环境变量
3. 点击 **Save Changes**
4. 服务会自动重启以应用新的环境变量

## 监控和维护

### 查看服务状态

Render Dashboard 提供：
- CPU 和内存使用情况
- 请求数量统计
- 响应时间监控
- 错误日志追踪

### 邮件通知

Render 会在以下情况发送邮件通知：
- 部署成功或失败
- 服务宕机
- 构建错误

## 成本估算

### 免费层限制

- ✅ 750 小时/月运行时间（足够 24/7 运行）
- ✅ 自动 HTTPS
- ✅ 无限带宽
- ⚠️ 15 分钟不活动后休眠
- ⚠️ 无持久化存储

### 升级选项

如果需要更好的性能，可以考虑：
- **Starter 方案**: $7/月，无休眠，512MB 内存
- **Standard 方案**: $25/月，2GB 内存，更好的性能
- **持久化磁盘**: $1-2/月/GB

## 其他部署选项

如果 Render 不满足需求，还可以考虑：

1. **Railway**: 类似 Render，有 $5/月免费额度，支持持久化存储
2. **Fly.io**: 免费额度较好，支持全球部署
3. **Heroku**: 经典选择，但免费层已取消
4. **AWS/GCP/Azure**: 更强大但配置更复杂

## 技术支持

- Render 官方文档：https://render.com/docs
- FastAPI 文档：https://fastapi.tiangolo.com/
- 遇到问题可以查看 Render 社区：https://community.render.com/

## 下一步

部署完成后，建议：
1. ✅ 在前端项目中配置后端 API 地址
2. ✅ 测试所有 API 端点
3. ✅ 配置监控和告警
4. ✅ 考虑添加 API 文档（FastAPI 自带 Swagger UI）
5. ✅ 根据需要配置数据持久化方案

祝部署顺利！🚀

