"""运行第 6 次课的全部检查点。"""

from coin_change import coin_dp, coin_greedy
from knapsack import DEFAULT_ITEMS, knapsack_01, sampled_last_row


def print_knapsack(title: str, capacity: int, required: tuple[str, ...] = ()) -> None:
    result = knapsack_01(DEFAULT_ITEMS, capacity, required)
    names = [item.name for item in result.selected_items]
    print(f"\n{title}")
    print(f"容量：{capacity}g")
    print(f"最大重要度：{result.max_value}")
    print(f"总重量：{result.total_weight}g")
    print(f"选择：{names}")
    if required:
        print(f"必选：{list(required)}")
    print("回溯：")
    for step in result.trace:
        print(
            f"  {step.item}: {step.decision} "
            f"(回溯容量 {step.capacity_before} -> {step.capacity_after})"
        )


def main() -> None:
    coins = [1, 5, 11]
    amount = 15
    greedy_count, greedy_combination = coin_greedy(coins, amount)
    dp_count, dp_combination = coin_dp(coins, amount)

    print("检查点 1：凑硬币")
    print(f"贪心：{greedy_count} 枚，组合 {greedy_combination}")
    print(f"动规：{dp_count} 枚，组合 {dp_combination}")

    standard = knapsack_01(DEFAULT_ITEMS, 1000)
    print_knapsack("检查点 2：标准 0-1 背包", 1000)
    print("\ndp 表最后一行（容量每 50g 采样）：")
    print(sampled_last_row(standard, step=50))

    print_knapsack("检查点 3：容量改为 800g", 800)
    print_knapsack("检查点 4：增加必选约束", 1000, ("炉具",))


if __name__ == "__main__":
    main()
