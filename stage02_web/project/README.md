# Todo 全栈参考项目

目录分工：`backend/` 是 FastAPI API，`frontend/` 是 Vue 3 页面，`compose.yaml` 编排两个独立镜像与 PostgreSQL。浏览器只访问前端，前端向 `/api` 发送请求；开发时由 Vite 转发，容器部署时由 Nginx 转发。

## 一键运行（需要 Docker）

在本目录执行：

```powershell
Copy-Item .env.example .env
# 编辑 .env，设置自己的 POSTGRES_PASSWORD
docker compose up --build -d
docker compose ps
```

页面：`http://localhost:8080`；API 文档：`http://localhost:8000/docs`。用页面新增任务后运行 `docker compose down`、`docker compose up -d`，任务仍在 PostgreSQL 的 `pgdata` 数据卷中。查看日志：`docker compose logs backend`、`docker compose logs frontend`、`docker compose logs db`。

## 分别打包

```powershell
docker build -t todo-backend:learn ./backend
docker build -t todo-frontend:learn ./frontend
```

两个镜像可分别构建、标记和发布。Compose 的 `build` 配置会在 `docker compose up --build` 时使用各自的 Dockerfile。修改 Vue 代码只需重建前端；修改 FastAPI 代码只需重建后端。

## 本地开发

先启动 PostgreSQL：`docker compose up -d db`。没有 Docker 时也可用本机 PostgreSQL，自行创建用户 `todo` 与数据库 `todo`。后端在 `backend/` 运行：

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
$env:DATABASE_URL='postgresql+psycopg://todo:你的密码@localhost:5432/todo'
.venv\Scripts\python -m uvicorn app.main:app --reload
```

另开终端，在 `frontend/` 运行 `npm ci`、`npm run dev`，打开 Vite 显示的地址（通常是 `http://localhost:5173`）。本地前端的 `/api` 经 Vite 转发到 `127.0.0.1:8000`。后端测试：在 `backend/` 执行 `.venv\Scripts\python -m pytest`。

若密码包含 `@`、`:`、`/` 等 URL 特殊字符，`DATABASE_URL` 中需要对密码进行 URL 编码；初学时可先使用只含字母和数字的练习密码。`.env` 不要提交到 Git。

## 数据与限制

- 示例用 SQLAlchemy `create_all` 创建初始表，尚未包含数据库迁移；已有数据的结构变化需要另学 Alembic。
- 当前没有认证与用户隔离，只适合本地学习；公网部署前先实现认证、HTTPS、备份和访问控制。
- 测试使用临时 SQLite 验证 API 逻辑；第 2、3 周要求额外在 PostgreSQL 上完成联调。
- 停止服务用 `docker compose down`；不要在保留数据时加 `--volumes`。
