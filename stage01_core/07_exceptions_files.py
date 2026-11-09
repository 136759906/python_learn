# -*- coding: utf-8 -*-
"""第 7 课：异常处理与文件读写"""

# ============================================================
# 知识点提示
# ============================================================
# 1. try / except / else / finally
# 2. 常见异常：ValueError, TypeError, FileNotFoundError, KeyError
# 3. with open(...) as f: 自动关闭文件
# 4. 模式："r" 读, "w" 覆盖写, "a" 追加
# 5. JSON: import json; json.dumps() / json.loads()
# 6. CSV: import csv; csv.reader() / csv.writer()

# ============================================================
# 【练习】
# ============================================================

# TODO 1: 安全地把字符串转成 int（失败返回 None）
def safe_int(text: str) -> int | None:
    pass

# TODO 2: 实现一个函数，读取一个文本文件，返回总行数
def count_lines(path: str) -> int:
    pass

# TODO 3: 实现一个函数，把 dict 列表写入 JSON 文件，再读回来并返回
def save_and_load_json(path: str, records: list[dict]) -> list[dict]:
    pass

# TODO 4: 实现一个函数，捕获除零错误并返回 "除数不能为 0"
def safe_divide(a: float, b: float) -> float | str:
    pass


if __name__ == "__main__":
    assert safe_int("42") == 42
    assert safe_int("abc") is None
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(1, 0) == "除数不能为 0"

    data = [{"name": "张三", "age": 28}]
    assert save_and_load_json("test_data.json", data) == data
    print("第 7 课全部通过！")
