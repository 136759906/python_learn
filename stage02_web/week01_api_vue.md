# 第 1 周：HTTP、FastAPI 与 Vue 3 入门

目标：理解浏览器怎样请求 API，写出第一个 FastAPI 路由和 Vue 3 组件。本周不要求数据库；先把前后端的边界搞清楚。每天约 1～2 小时。

## 第 1 天：HTTP 与第一个 API

请求包含方法、路径和可选的请求体；响应包含状态码和响应体。在 `stage02_web/` 创建 `hello.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

安装 `fastapi uvicorn`，运行 `python -m uvicorn hello:app --reload`，访问 `http://127.0.0.1:8000/docs`。练习：增加 `/api/hello/{name}`。验收：正常路径返回 200，不存在的路径返回 404；能解释 GET 为什么不需要请求体。

## 第 2 天：路径、查询参数和校验

在 `hello.py` 增加 `@app.get("/api/times/{count}")`，让 `count: int` 决定重复次数，再增加 `upper: bool = False` 查询参数。练习：比较 `/api/times/2?upper=true` 与 `/api/times/abc`。验收：知道 422 表示输入没有通过校验，并能在 `/docs` 找到自动生成的参数说明。

## 第 3 天：Vue 3 的组件和响应式状态

先使用仓库的 `project/frontend/`；运行 `npm install`、`npm run dev`。阅读 `src/main.js` 与 `src/App.vue`，了解组件、`<script setup>`、模板、`ref`。在组件里增加：

```vue
<script setup>
import { ref } from 'vue'
const message = ref('你好，Vue')
</script>

<template>
  <input v-model="message" />
  <p>{{ message }}</p>
</template>
```

练习时可暂时替换 `App.vue`，完成后从 Git 恢复课程示例。验收：输入框内容变化时页面立即变化；能指出 `ref`、`v-model`、模板插值各自作用。

## 第 4 天：列表、事件和计算属性

在 `App.vue` 中观察 `v-for`、`:key`、`@click`、`computed`。先使用静态的任务数组，点按钮切换 `done`，再显示未完成数量。验收：列表和数量一起更新；每条记录使用稳定的 `id` 作为 key。

## 第 5 天：浏览器访问 API

阅读 `project/frontend/vite.config.js` 中的 `/api` 开发代理。启动第 1 天的 API 和 Vue 开发服务器，在组件中调用 `fetch('/api/health')`，显示 `status`。练习：关闭 API 服务，给页面加加载中和失败提示。验收：在浏览器开发者工具 Network 面板看到请求与状态码；理解前端不能直接访问数据库。

> 开发代理把浏览器的 `/api` 请求转发到后端。后面 Docker 部署时由独立的 Nginx 前端容器完成同样的转发；前后端仍分别构建和部署。

参考：[FastAPI 教程](https://fastapi.tiangolo.com/tutorial/)、[Vue 3 快速开始](https://vuejs.org/guide/quick-start.html)、[Vue 响应式基础](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)。
