# 项目 3：命令行记账工具

## 目标

实现 `expense.py`，支持记账、统计、按月查询、数据导出。

## 功能要求

1. **添加记录**：`python expense.py add 35.5 午饭 --category 餐饮 --date 2026-11-09`
2. **列出记录**：`python expense.py list [--month 2026-11]`，按日期倒序显示
3. **统计**：`python expense.py stats [--month 2026-11]`，输出总支出、各分类支出占比
4. **导出**：`python expense.py export --format csv`，导出为 CSV
5. **数据持久化**：数据存 `expenses.json`

## 技术要点

- 用 `class Expense` 封装单条记录（用第 8 课的知识）
- 用 `class ExpenseBook` 封装所有操作（增删查统计导出）
- 用 `defaultdict` 做分类统计
- 用 `csv.writer` 导出 CSV
- 合理拆分函数，每个函数只做一件事

## 加分项（可选）

- 支持 `--sort amount/category` 排序参数
- 支持 `list --limit 10` 只显示最近 10 条
- 为 `ExpenseBook` 写 pytest 单元测试
