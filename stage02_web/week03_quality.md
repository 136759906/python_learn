# 第 3 周：错误处理、测试与前后端边界

目标：让待办应用在异常输入和服务故障时仍有明确行为，并能用测试验证关键 API。本周的示例工程不含登录；认证与用户隔离留作完成基础项目后的扩展，避免把数据库、前端和 JWT 同时引入。

## 第 11 天：HTTP 错误和输入边界

比较 `POST /api/tasks` 提交空标题、空格标题、101 字标题，以及 `PATCH /api/tasks/999`。阅读后端 `TaskCreate` 和 `HTTPException`。练习：增加一条测试，要求标题包含换行时被拒绝。验收：错误请求不写入 PostgreSQL，状态码和错误信息可解释。

## 第 12 天：前端的加载、空列表和失败状态

阅读 `App.vue` 的 `loading`、`saving`、`error`。练习：关闭后端后刷新页面，观察错误；打开后端再刷新恢复。给更新、删除按钮增加操作中禁用状态，避免快速连点。验收：用户能区分“还没有任务”和“请求失败”。

## 第 13 天：API 自动化测试

在 `project/backend/` 安装 `pytest httpx`，运行 `python -m pytest`。阅读 `tests/test_tasks.py`，理解测试数据库、依赖覆盖、正常路径与异常路径。练习：新增一个测试，验证标题长度超过 100 被拒绝。验收：测试可反复运行，且不修改开发用 PostgreSQL 数据。

## 第 14 天：PostgreSQL 集成核对

自动测试使用 SQLite 验证逻辑，不能替代 PostgreSQL 集成检查。用实际 PostgreSQL 再执行一遍创建、更新、删除，并检查重启后持久化。练习：故意设置错误密码，观察后端日志与 HTTP 结果。验收：能区分连接失败、校验失败与业务 404。

## 第 15 天：边界与安全入门

浏览器只调用后端 API；数据库密码只存在后端环境变量；前端代码和构建产物中不得包含密码。用开发者工具检查前端请求。练习：在 README 写出“用户 A 不能修改用户 B 的任务”需要哪些后端改动（用户表、登录、`user_id` 过滤和权限测试）。验收：明确当前示例**没有认证，不应直接暴露到公网**。

参考：[FastAPI 测试](https://fastapi.tiangolo.com/tutorial/testing/)、[FastAPI 错误处理](https://fastapi.tiangolo.com/tutorial/handling-errors/)。
