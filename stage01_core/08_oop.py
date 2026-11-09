# -*- coding: utf-8 -*-
"""第 8 课：面向对象编程"""

# ============================================================
# 知识点提示
# ============================================================
# 1. class 定义类，__init__ 是构造方法
# 2. self 指实例自身
# 3. 实例方法 / 类方法 / 静态方法
# 4. 继承：class Child(Parent):
# 5. 魔法方法：__str__ / __repr__ / __eq__ / __len__
# 6. property 装饰器：把方法伪装成只读属性

# ============================================================
# 【练习】实现一个银行账户类
# ============================================================

# TODO: 实现 BankAccount 类
# 要求：
#   1. __init__ 接收 owner 和 balance（默认 0）
#   2. deposit(amount) 存钱，金额必须为正数，否则抛 ValueError
#   3. withdraw(amount) 取钱，余额不足抛 ValueError
#   4. 添加只读属性 balance_info，返回 "owner 的余额为 xx 元"
#   5. __str__ 返回 "BankAccount(owner, balance)"
class BankAccount:
    pass


# ============================================================
# 【练习】继承练习
# ============================================================

# TODO: 实现 SavingsAccount（储蓄账户），继承 BankAccount
# 额外功能：add_interest(rate) 按利率增加余额（rate 为小数，如 0.03 表示 3%）
class SavingsAccount(BankAccount):
    pass


if __name__ == "__main__":
    account = BankAccount("张三", 100)
    account.deposit(50)
    assert account.balance == 150
    account.withdraw(30)
    assert account.balance == 120
    assert account.balance_info == "张三 的余额为 120 元"
    assert str(account) == "BankAccount(张三, 120)"

    try:
        account.withdraw(999)
        raise AssertionError("应该抛出 ValueError")
    except ValueError:
        pass

    savings = SavingsAccount("李四", 1000)
    savings.add_interest(0.03)
    assert savings.balance == 1030
    print("第 8 课全部通过！")
