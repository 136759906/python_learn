# -*- coding: utf-8 -*-
"""第 4 课：循环"""

# ============================================================
# 知识点提示
# ============================================================
# 1. for 循环遍历序列
# 2. range(start, stop, step)
# 3. while 循环
# 4. break 与 continue
# 5. enumerate() 同时取下标和值
# 6. zip() 同时遍历多个序列

# ============================================================
# 【练习】
# ============================================================

# TODO 1: 计算 1 到 100 的和（用 for 循环）
def sum_1_to_100() -> int:
    pass

# TODO 2: 返回九九乘法表，共 9 行，每行是一个字符串
# 第 1 行: "1*1=1"
# 第 2 行: "1*2=2 2*2=4"
# 第 9 行: "1*9=9 2*9=18 ... 9*9=81"
def multiplication_table() -> list[str]:
    pass

# TODO 3: 找出 100 以内（不含 100）所有能被 3 整除但不能被 5 整除的数
def fizz_3_not_5() -> list[int]:
    pass

# TODO 4: 用 while 循环实现：不断把 n 除以 2，直到 n < threshold，返回除了多少次
def halve_until_small(n: int, threshold: int = 10) -> int:
    pass


if __name__ == "__main__":
    assert sum_1_to_100() == 5050
    assert multiplication_table()[0] == "1*1=1"
    assert multiplication_table()[8] == "1*9=9 2*9=18 3*9=27 4*9=36 5*9=45 6*9=54 7*9=63 8*9=72 9*9=81"
    assert fizz_3_not_5()[:4] == [3, 6, 9, 12]
    assert halve_until_small(1024) == 7
    print("第 4 课全部通过！")
