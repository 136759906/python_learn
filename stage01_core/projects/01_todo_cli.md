# 项目 1：待办清单 CLI

## 目标

实现一个命令行待办清单程序 `todo.py`，支持增删改查和数据持久化。

## 功能要求

1. **添加任务**：`python todo.py add "买牛奶"`，显示"已添加：买牛奶"
2. **列出任务**：`python todo.py list`，显示所有任务，格式 `1. [ ] 买牛奶`
3. **完成标记**：`python todo.py done 1`，将第 1 条任务标记为 `[x]`
4. **删除任务**：`python todo.py remove 1`，删除第 1 条任务
5. **数据持久化**：把任务保存到 `todos.json`，重启后数据不丢失

## 技术要点

- 使用 `argparse` 或直接读取 `sys.argv` 处理命令行参数
- 使用 `json` 模块读写文件
- 使用 `try/except` 处理文件不存在的情况
- 任务数据结构：`[{"text": "买牛奶", "done": false}]`
