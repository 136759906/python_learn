# -*- coding: utf-8 -*-
"""第 6 课：list / tuple / dict / set、切片与推导式"""

# ============================================================
# 知识点提示
# ============================================================
# list:  有序、可变，[1, 2, 3]
# tuple: 有序、不可变，(1, 2, 3)
# dict:  键值对，{"name": "张三", "age": 28}
# set:   无序、不重复，{1, 2, 3}
# 切片:  lst[1:4]  lst[::-1]  lst[::2]
# 推导式: [x*x for x in range(10) if x % 2 == 0]

# ============================================================
# 【练习】
# ============================================================

# TODO 1: 反转列表 [1,2,3,4,5]（不要用 reverse() 方法）
def reverse_list(items: list[int]) -> list[int]:
    pass

# TODO 2: 统计字符串中每个字符出现的次数，返回 dict
def char_count(text: str) -> dict[str, int]:
    pass

# TODO 3: 两个列表去重合并（保持顺序，用列表实现）
def merge_unique(list_a: list, list_b: list) -> list:
    pass

# TODO 4: 用推导式生成 1-30 中所有能被 4 整除的数的平方
def squares_of_multiples_of_4() -> list[int]:
    pass

# TODO 5: 合并两个字典，相同键时取较大值
def merge_max(dict_a: dict, dict_b: dict) -> dict:
    pass


if __name__ == "__main__":
    assert reverse_list([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]
    assert char_count("hello") == {"h": 1, "e": 1, "l": 2, "o": 1}
    assert merge_unique([1, 2, 3], [3, 4, 5]) == [1, 2, 3, 4, 5]
    assert squares_of_multiples_of_4()[:3] == [16, 64, 144]
    assert merge_max({"a": 1, "b": 2}, {"b": 5, "c": 9}) == {"a": 1, "b": 5, "c": 9}
    print("第 6 课全部通过！")
