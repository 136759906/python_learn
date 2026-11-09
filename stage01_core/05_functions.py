# -*- coding: utf-8 -*-
"""第 5 课：函数"""

# ============================================================
# 知识点提示
# ============================================================
# 1. def 定义函数
# 2. 位置参数 / 默认参数 / 关键字参数
# 3. *args 接收任意个位置参数
# 4. **kwargs 接收任意个关键字参数
# 5. 返回多个值（本质是元组）
# 6. lambda 表达式
# 7. 类型注解：def add(a: int, b: int) -> int:

# ============================================================
# 【练习】
# ============================================================

# TODO 1: 实现一个函数，接收任意个数字，返回它们的平均值
def average(*numbers: float) -> float:
    pass

# TODO 2: 实现一个函数，返回两个数的和与差（多返回值）
def sum_diff(a: float, b: float) -> tuple[float, float]:
    pass

# TODO 3: 实现一个函数，接收一个列表和一个函数，返回应用函数后的新列表
# 类似 map 的效果，但不使用 map
def apply_all(items: list, func) -> list:
    pass

# TODO 4: 用 lambda 实现：返回 a 的 b 次方
power = None


if __name__ == "__main__":
    assert average(1, 2, 3) == 2.0
    assert average(10, 20, 30, 40) == 25.0
    assert sum_diff(10, 3) == (13, 7)
    assert apply_all([1, 2, 3], lambda x: x * 2) == [2, 4, 6]
    assert power(2, 3) == 8
    print("第 5 课全部通过！")
