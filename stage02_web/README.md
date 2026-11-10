# 阶段二：FastAPI + Vue 3 + PostgreSQL 全栈课程

本阶段学习一个**前后端分离**的待办清单项目：FastAPI 提供 JSON API，Vue 3 负责页面，PostgreSQL 保存数据。前端与后端分别构建 Docker 镜像，再通过 Docker Compose 和数据库一起运行。建议先完成阶段一的函数、类、异常、JSON 和文件练习。

## 开始前

- Python 3.10+、Node.js/npm、PostgreSQL；第 4 周需要 Docker Engine 与 Docker Compose。
- 没有本机 PostgreSQL 时，可先用 `docker compose up -d db` 启动数据库。
- 先阅读 [参考项目说明](project/README.md)，再按周学习。参考项目是最终形态；每周只关注当周的文件和功能，不要求第一天读懂全部代码。
- 每天约 1～2 小时。四周是基础学习计划，项目打磨和进阶功能可另留 1～2 周。

## 四周课程

| 周 | 每日主题 | 课程 | 本周验收 |
|---|---|---|---|
| 1 | HTTP、FastAPI 路由、Vue 组件、响应式、前后端请求 | [第 1 周](week01_api_vue.md) | Vue 页面能显示 API 状态 |
| 2 | PostgreSQL、表与 SQL、ORM CRUD、Pydantic、Vue 表单 | [第 2 周](week02_postgres_crud.md) | 页面操作写入 PostgreSQL，重启后数据仍在 |
| 3 | 输入边界、前端状态、自动化测试、PG 集成检查、安全边界 | [第 3 周](week03_quality.md) | 正常与异常 API 测试通过，能定位失败原因 |
| 4 | 前后端分别构建、Compose 网络、PG 数据卷、部署排障 | [第 4 周](week04_docker.md) | 三个容器运行，重启后任务仍在 |

## 学习方式

每天按“读概念 → 运行示例 → 自己修改 → 按验收点检查”进行。浏览器开发者工具看请求与状态码；FastAPI `/docs` 用来验证接口；`psql` 用来核对数据库。前端不直接访问 PostgreSQL，数据库密码只交给后端。

Jupyter 适合单独试 Python 语法和 SQL 结果；本阶段的服务、Vue 页面和 Docker 操作请在终端运行，保留两个服务的日志。遇到错误时先确定是在浏览器、API 还是数据库层。

## 基础通关与进阶

基础通关：完成 CRUD、输入校验、Vue 页面、PostgreSQL 持久化、后端测试和分别构建的 Docker 镜像。此时项目适合本地学习演示，**没有登录与用户隔离，不能直接公开部署**。

进阶顺序：[面试题](interview_questions.md) → 用户登录与任务归属 → 数据库迁移 → HTTPS/备份 → 缓存、限流与监控。原有面试题是进阶复习材料，其中 Redis、JWT、生产部署等内容不作为本阶段基础通关的前置条件。
