"""凑硬币：比较贪心法与动态规划法。"""

from __future__ import annotations

from math import inf
from typing import Iterable


def _normalise_coins(coins: Iterable[int]) -> tuple[int, ...]:
    """校验面额并返回从大到小排列、去重后的元组。"""
    normalised = tuple(sorted(set(coins), reverse=True))
    if not normalised or any(not isinstance(coin, int) or coin <= 0 for coin in normalised):
        raise ValueError("硬币面额必须是非空的正整数集合")
    return normalised


def _validate_amount(amount: int) -> None:
    if not isinstance(amount, int) or amount < 0:
        raise ValueError("金额必须是非负整数")


def coin_greedy(coins: Iterable[int], amount: int) -> tuple[int, list[int]]:
    """每次取不超过余额的最大面额；无法恰好凑出时抛出异常。"""
    ordered = _normalise_coins(coins)
    _validate_amount(amount)

    remaining = amount
    combination: list[int] = []
    for coin in ordered:
        count, remaining = divmod(remaining, coin)
        combination.extend([coin] * count)

    if remaining != 0:
        raise ValueError(f"贪心法无法用 {list(ordered)} 恰好凑出 {amount}")
    return len(combination), combination


def coin_dp(coins: Iterable[int], amount: int) -> tuple[int, list[int]]:
    """用自底向上的动态规划求最少硬币数及一组最优组合。"""
    ordered = tuple(sorted(_normalise_coins(coins)))
    _validate_amount(amount)

    dp = [inf] * (amount + 1)
    previous_coin: list[int | None] = [None] * (amount + 1)
    dp[0] = 0

    for current in range(1, amount + 1):
        for coin in ordered:
            if coin > current:
                break
            candidate = dp[current - coin] + 1
            if candidate < dp[current]:
                # 关键填表行：由较小金额的最优解推出当前金额的最优解。
                dp[current] = candidate
                previous_coin[current] = coin

    if dp[amount] == inf:
        raise ValueError(f"无法用 {list(ordered)} 恰好凑出 {amount}")

    combination: list[int] = []
    current = amount
    while current > 0:
        coin = previous_coin[current]
        if coin is None:  # 防御性检查，正常路径不会到这里。
            raise RuntimeError("动态规划回溯失败")
        combination.append(coin)
        current -= coin

    combination.sort(reverse=True)
    return int(dp[amount]), combination


if __name__ == "__main__":
    test_coins = [1, 5, 11]
    test_amount = 15
    print("贪心：", coin_greedy(test_coins, test_amount))
    print("动规：", coin_dp(test_coins, test_amount))
