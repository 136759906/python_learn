# Web 后端面试题（生产实战版）

每完成一周课程，就过一遍对应题目。答案按"生产中怎么做 + 会踩什么坑"组织，
面试时按这个思路回答，比背概念高一个档次。

## 一、异步与并发（第一周）

### 1. FastAPI 中 `async def` 和 `def` 路由有什么区别？

**生产答案：**

- `async def` 运行在事件循环中，适合 IO 密集且所有依赖都是异步库（`AsyncSession`、`httpx.AsyncClient`、`redis.asyncio`）
- `def` 会被 FastAPI 自动丢进线程池执行，适合同步 ORM（SQLAlchemy 同步模式）、调用阻塞 SDK
- **最大的坑**：在 `async def` 里调用同步阻塞函数（`time.sleep`、`requests`、同步 DB），整个事件循环被卡住，所有并发用户一起变慢

**规则：** `async def` 里只 `await`，不出现任何同步阻塞调用；拿不准就用 `def`。

**追问：** 为什么 `requests` 不行？因为它是同步库，发出请求后事件循环被挂起；换 `httpx.AsyncClient` + `await`。

### 2. GIL 对 Web 服务性能有什么影响？

**生产答案：**

- GIL 只允许一个线程同时执行 Python 字节码
- Web 接口大多数是 IO 密集（等数据库、等下游 HTTP），IO 期间释放 GIL，所以影响不大
- CPU 密集任务（报表计算、加解密）在异步服务里会阻塞事件循环；生产做法是拆成独立进程/任务队列（Celery、RQ）

**追问：** 那部署时怎么扩展？Gunicorn 起多个 worker 进程（通常 worker 数 = CPU 核数 × 1~2，IO 密集可以更多），每个 worker 内部再跑异步事件循环。

### 3. WSGI 和 ASGI 的区别？FastAPI 属于哪种？

**生产答案：**

- WSGI（Django/Flask 传统模式）：同步协议，一个请求占一个进程/线程，靠多 worker 抗并发
- ASGI（FastAPI/Starlette）：异步协议，支持 WebSocket、长连接、事件循环内高并发 IO
- FastAPI 是 ASGI 框架，生产上通常用 Gunicorn 管理 Uvicorn worker

### 4. 线上接口突然变慢（RT 从 50ms 涨到 3s），你怎么排查？

**生产答案（面试官想听到的是排查框架，不是猜答案）：**

1. **先看大盘**：是全量接口慢还是个别接口慢？
   - 全量慢 → 公共依赖问题：数据库（慢查询、连接池耗尽）、Redis、网络
   - 个别慢 → 该接口自身问题：数据量涨了、新上的代码、索引失效
2. **看资源指标**：CPU、内存、DB 连接数、QPS 有没有突变（是不是流量高峰）
3. **开慢查询日志**：`EXPLAIN` 看执行计划，是不是全表扫描、`Using filesort`
4. **看日志里的耗时分布**：数据库耗时 vs 业务计算 vs 外部调用
5. **临时缓解**：限流、降级非核心功能、扩容 worker；同时并行查根因

**加分点**：说"我会给每个中间件调用加耗时日志，提前埋点，出事才有数据可查"。

## 二、数据库与 ORM（第二周）

### 5. 什么是 N+1 查询问题？怎么发现、怎么解决？

**生产答案：**

- **现象**：查一页 20 篇文章（1 条 SQL），每篇文章再查作者（20 条 SQL）→ 共 21 条
- **发现**：开启 SQLAlchemy echo 日志；或对高频接口数一下 SQL 条数；生产用 APM 统计
- **解决**：
  - 一对多：`selectinload(Author.articles)`，用 `WHERE id IN (...)` 一次查回
  - 多对一/一对一：`joinedload`，JOIN 一次查出
  - 小数据量：手动收集 id 批量查，组装 dict

**追问：** joinedload 和 selectinload 怎么选？
- joinedload：关联数据小、单条记录场景（一对一）
- selectinload：一对多，JOIN 会产生笛卡尔积膨胀，IN 查询更划算

### 6. 数据库连接池怎么配置？连接池大小有公式吗？

**生产答案：**

- 关键参数：`pool_size`（常驻连接）、`max_overflow`（峰值允许超配）、`pool_timeout`（等连接的超时）、`pool_recycle`（连接最大存活时间）
- **总量约束**：`Gunicorn worker 数 × (pool_size + max_overflow) ≤ 数据库 max_connections`
- **为什么需要 pool_recycle**：MySQL 默认 8 小时无活动会主动断连，池里的连接失效后报 `MySQL server has gone away`；生产设 `pool_recycle=3600`
- 不是越大越好：连接太多会拖垮数据库的调度和内存，IO 密集型服务通常 pool_size 5-20 起步，压测调整

### 7. SQLAlchemy Session 的正确生命周期是什么？

**生产答案：**

- **一次请求一个 Session**，用依赖注入 `yield`：

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- Session 不是线程安全的，绝不能全局共享一个 Session
- 写操作集中在请求末尾统一 `commit`；出现异常统一 `rollback`
- **坑**：`commit` 后对象变为 detached，模板/序列化再访问懒加载属性会报错，必要时用 `db.refresh(obj)` 或预加载

### 8. 事务边界怎么设计？什么情况会锁表？

**生产答案：**

- 事务要短：把 HTTP 调用、慢计算放在事务外，只包住写库部分
- 悲观锁（`SELECT ... FOR UPDATE`）：短事务内锁定行，注意必须走索引，否则可能锁全表
- 乐观锁（version 字段）：更新时 `WHERE version = ?`，失败重试，适合低冲突场景
- 分布式场景：优先用"本地事务 + 消息队列最终一致"，不要硬上 2PC

### 9. 索引怎么设计？索引为什么会失效？

**生产答案：**

- 建索引的依据：`WHERE`、`JOIN`、`ORDER BY` 高频字段；区分度高的列优先
- 联合索引最左匹配：`INDEX(a, b)` 支持 `WHERE a=?` 和 `WHERE a=? AND b=?`，不支持 `WHERE b=?`
- 失效场景：对索引列用函数/运算（`WHERE YEAR(create_time)=2026`）、隐式类型转换（字符串列传数字）、前导模糊匹配（`LIKE '%xx'`）、OR 连接非索引列
- 排查工具：`EXPLAIN`，重点看 `type`（至少 range）、`rows`、`Extra`（`Using filesort` / `Using temporary` 要警惕）

## 三、认证与安全（第三周）

### 10. JWT 认证的完整流程？token 泄露怎么办？

**生产答案：**

- 流程：登录校验 → 服务端用密钥签发 access token（短，如 30 分钟）+ refresh token（长，如 7 天）→ 客户端每次请求带 `Authorization: Bearer <token>` → 服务端验签 + 读 payload 里的 user_id
- **JWT 无法主动失效**（无状态签名），所以生产方案：
  - access token 短有效期，泄露损失有限
  - 用户改密码/登出时，把 token 版本号写入 Redis 黑名单，校验时先查黑名单
  - refresh token 一次一换，旧 token 立即作废

### 11. 什么是越权漏洞？怎么防？

**生产答案：**

- 水平越权：A 用户访问 B 用户的订单（`/orders/123` 没校验属主）
- 垂直越权：普通用户调用管理员接口
- **核心防线：所有查询强制带属主过滤**，不信任前端传来的任何数据：

```python
order = db.scalar(
    select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
)
```

- 管理接口用角色依赖统一拦截，不要在 handler 里散落 if

### 12. CSRF 和 XSS 的区别？前后端分离项目还需要防 CSRF 吗？

**生产答案：**

- XSS：恶意脚本被注入页面执行。后端配合：响应头 `Content-Type` 正确、富文本入库前消毒、关键 Cookie 加 `HttpOnly`
- CSRF：诱导已登录用户的浏览器发跨站请求。经典方案是 CSRF token
- 前后端分离 + token 放 Header（不用 Cookie 自动携带）时，天然免疫传统 CSRF，但要防 CORS 配错：`Access-Control-Allow-Origin` 生产环境绝不设为 `*` 同时 `allow-credentials=true`

### 13. 接口幂等性怎么设计？支付接口防重复扣款怎么做？

**生产答案：**

- 幂等 = 同一请求执行一次和执行多次结果相同
- 支付场景完整方案：
  1. 客户端提交订单时生成唯一幂等键（UUID）
  2. 服务端 `Redis SETNX idem_key`，设置过期时间（如 10 分钟）
  3. 抢到键的请求执行业务；已存在则返回上次结果
  4. **数据库唯一索引兜底**（订单号唯一），Redis 挂了也挡得住重复
  5. 结果落库时记录幂等键，保证响应可恢复

### 14. 限流怎么做？单机和分布式有什么区别？

**生产答案：**

- 算法：固定窗口（有临界突刺）、滑动窗口、漏桶（恒定速率）、令牌桶（允许突发，最常用）
- 单机：内存令牌桶
- **分布式：Redis + Lua** 保证"扣减计数"原子性，多实例共享同一配额
- 分层：网关层限总流量（防攻击），应用层按用户/API key 限流（保公平）
- 返回 429 + `Retry-After`，前端做退避重试

### 15. 缓存穿透、击穿、雪崩分别怎么处理？

**生产答案：**

| 问题 | 场景 | 方案 |
|------|------|------|
| 穿透 | 查不存在的 key，每次都打穿到 DB | 空结果也短暂缓存；布隆过滤器前置 |
| 击穿 | 热点 key 过期瞬间大量请求同时打 DB | 互斥锁重建（只放一个请求去查）；逻辑过期不删 key |
| 雪崩 | 大量 key 同时过期 | 过期时间加随机抖动；多级缓存（本地 + Redis）；熔断降级 |

### 16. 生产环境有哪些"隐形"安全问题？

**生产清单：**

- SQL 注入：ORM 参数化查询（不用字符串拼 SQL）
- 密钥管理：数据库密码、JWT 密钥放环境变量/密钥管理服务，绝不进 Git
- 日志脱敏：密码、token、手机号、身份证号不能明文进日志
- 错误信息不外泄：500 只返回通用提示，堆栈只进日志
- 依赖安全：定期升级依赖，用 pip-audit 查已知漏洞
- 文件上传：校验类型、大小限制、存独立存储（不存 Web 目录）、文件名不可控

## 四、测试与部署（第四周）

### 17. 测试怎么写才有价值？（测试金字塔）

**生产答案：**

- **单元测试**（多）：核心业务逻辑、工具函数，快、稳定、不依赖外部
- **接口测试**（中）：TestClient + 临时数据库（每用例隔离），覆盖正常路径 + 401/403/404/422
- **端到端**（少）：关键流程（登录→下单→支付回调）
- 反模式：只测 HTTP 200，不测数据真实写入；mock 掉一切导致测试全绿但线上全挂
- **要点**：测试数据库要和正式库同类型（用 SQLite 测不出 MySQL 的行为差异），用事务回滚或 truncate 隔离数据

### 18. Docker 镜像和部署怎么配置？

**生产答案：**

- 多阶段构建：builder 阶段装依赖，运行阶段只拷贝产物，镜像更小
- `python:3.12-slim` 起步，不用 full 版本
- requirements 锁定版本号，配合国内镜像源
- 健康检查 `/health`，编排时 DB 就绪才启动应用
- Gunicorn 命令：`gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000`
- worker 数按 CPU 与 IO 特性定，压测验证，不迷信公式

### 19. 日志和可观测性怎么做才算生产级？

**生产答案：**

- 结构化日志（JSON），带 `request_id`、`user_id`、`path`、`status`、`耗时`
- 访问日志 + 业务日志 + SQL 慢日志分层
- 基本三件套：日志（出事后查原因）、指标（QPS/RT/错误率，看趋势）、追踪（跨服务调用链）
- 预设告警：错误率突增、RT 超阈值、连接池饱和

### 20. 你的项目怎么证明达到生产标准？

**面试时这样答（对照自己项目准备）：**

- 打开 Swagger 文档，讲清楚每个接口的请求/响应模型
- 演示认证流程：无 token 访问返回 401，用户 A 访问用户 B 的数据返回 404（不是 403，因为对属主来说"资源不存在"）
- 展示 SQL 日志：列表接口只有 2 条 SQL，无 N+1
- 展示限流：压测返回 429
- 展示测试覆盖率：核心路径有测试
- 一键 `docker compose up` 启动全套环境
