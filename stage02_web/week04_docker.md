# 第 4 周：前后端分别打包并用 Docker 部署

目标：理解三个服务各自负责什么，分别构建后端与前端镜像，再通过 Compose 启动 FastAPI、Vue 静态站点和 PostgreSQL。先在本机演练；部署到服务器前补齐 HTTPS、认证和备份。

## 第 16 天：读懂三个容器

`backend/Dockerfile` 只安装 Python 依赖并运行 Uvicorn；`frontend/Dockerfile` 第一阶段用 Node 构建 Vue，第二阶段用 Nginx 提供静态文件；`db` 使用 PostgreSQL 镜像。练习：列出每个容器的入口、端口和需要的环境变量。验收：能解释为什么前端镜像里不应该有数据库密码。

## 第 17 天：分别构建镜像

在 `project/` 执行：

```powershell
docker build -t todo-backend:learn ./backend
docker build -t todo-frontend:learn ./frontend
docker image ls todo-backend todo-frontend
```

练习：修改 `App.vue` 文案，只重建前端镜像；修改 API 响应，只重建后端镜像。验收：能说明“构建镜像”和“运行容器”的区别；两个镜像可单独构建。

## 第 18 天：Compose 网络与数据卷

复制 `.env.example` 为 `.env` 并设置密码，然后 `docker compose up --build -d`。访问前端 `http://localhost:8080` 和 API 文档 `http://localhost:8000/docs`。浏览器请求 `/api/tasks` 会先到前端 Nginx，再转发到 `backend:8000`；后端使用 `db:5432` 访问 PostgreSQL。执行 `docker compose ps`、`docker compose logs backend`。验收：三个服务正常启动并能创建任务。

## 第 19 天：持久化与故障排查

创建任务后执行 `docker compose down`，再 `docker compose up -d`，确认任务仍在：`pgdata` 命名卷保存数据。若前端出现 502，先检查后端日志；若后端数据库连接失败，检查 DB 健康状态和 `DATABASE_URL`。验收：能根据容器日志定位服务故障。

> `docker compose down --volumes` 会删除数据库卷和数据，只在明确需要清空练习环境时使用。本课程验证持久化时不要加 `--volumes`。

## 第 20 天：部署清单与最终验收

分别打包两个镜像，记录镜像标签；配置独立的 PostgreSQL 数据卷和不提交 Git 的 `.env`。演示“新增 → 完成 → 刷新 → 停止/重启容器 → 数据仍在”。最终 README 应包含构建、启动、日志、停止、备份与恢复命令。公网部署前增加 HTTPS、认证、数据库备份和环境隔离；当前示例用于本地学习。

参考：[Docker 多阶段构建](https://docs.docker.com/build/building/multi-stage/)、[Docker Compose](https://docs.docker.com/compose/)、[PostgreSQL Docker 镜像](https://hub.docker.com/_/postgres)。
