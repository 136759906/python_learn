# -*- coding: utf-8 -*-
"""第 9 课：装饰器、生成器、迭代器、类型注解与模块"""

import time

# ============================================================
# 知识点提示
# ============================================================
# 1. 装饰器：接收函数并返回新函数，用 @ 语法
# 2. 生成器：yield 产出值，惰性计算，节省内存
# 3. 迭代器：实现 __iter__ 和 __next__
# 4. 类型注解：int, str, list[int], dict[str, int]
# 5. 模块：import / from ... import ... / as 别名
# 6. 常用内置函数：map, filter, zip, any, all, sorted(key=...)

# ============================================================
# 【练习】
# ============================================================

# TODO 1: 写一个装饰器 timer，记录被装饰函数的执行时间
def timer(func):
    pass

# TODO 2: 写一个生成器 fib()，不断产出斐波那契数列（从 1 开始）
def fib():
    pass

# TODO 3: 写一个函数，用 filter 和 lambda 找出列表中的所有偶数
def filter_evens(numbers: list[int]) -> list[int]:
    pass

# TODO 4: 用 sorted + lambda 把学生列表按成绩从高到低排序
def sort_students(students: list[dict]) -> list[dict]:
    pass


if __name__ == "__main__":
    @timer
    def slow_add(a, b):
        time.sleep(0.1)
        return a + b

    result = slow_add(1, 2)
    assert result == 3

    fib_gen = fib()
    first_8 = [next(fib_gen) for _ in range(8)]
    assert first_8 == [1, 1, 2, 3, 5, 8, 13, 21]

    assert filter_evens([1, 2, 3, 4, 5, 6]) == [2, 4, 6]

    students = [
        {"name": "A", "score": 80},
        {"name": "B", "score": 95},
        {"name": "C", "score": 88},
    ]
    assert sort_students(students)[0]["name"] == "B"
    print("第 9 课全部通过！")
