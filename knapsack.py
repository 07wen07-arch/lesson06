"""0-1 背包、容量变式和必选物品约束。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Item:
    name: str
    weight: int
    value: int


@dataclass(frozen=True)
class BacktrackStep:
    item: str
    decision: str
    capacity_before: int
    capacity_after: int


@dataclass
class KnapsackResult:
    max_value: int
    total_weight: int
    selected_items: list[Item]
    table: list[list[int]]
    trace: list[BacktrackStep]
    table_capacity: int


DEFAULT_ITEMS = [
    Item("帐篷", 300, 90),
    Item("炉具", 200, 60),
    Item("睡袋", 350, 115),
    Item("食物", 400, 120),
    Item("水具", 250, 80),
]


def _validate(items: list[Item], capacity: int) -> None:
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError("容量必须是非负整数")
    if len({item.name for item in items}) != len(items):
        raise ValueError("物品名称不能重复")
    if any(item.weight <= 0 or item.value < 0 for item in items):
        raise ValueError("物品重量必须为正数，价值不能为负数")


def knapsack_01(
    items: Iterable[Item],
    capacity: int,
    required_names: Iterable[str] = (),
) -> KnapsackResult:
    """求“至多装满”的 0-1 背包最优解。

    required_names 中的物品必须选择。实现方法是先放入所有必选物品，
    再用剩余容量对其余物品执行标准 0-1 背包动态规划。
    """
    item_list = list(items)
    _validate(item_list, capacity)

    required = set(required_names)
    known_names = {item.name for item in item_list}
    unknown = required - known_names
    if unknown:
        raise ValueError(f"不存在的必选物品：{sorted(unknown)}")

    required_items = [item for item in item_list if item.name in required]
    optional_items = [item for item in item_list if item.name not in required]
    required_weight = sum(item.weight for item in required_items)
    required_value = sum(item.value for item in required_items)
    if required_weight > capacity:
        raise ValueError("必选物品总重量超过容量")

    remaining_capacity = capacity - required_weight
    table = [[0] * (remaining_capacity + 1) for _ in range(len(optional_items) + 1)]

    for row, item in enumerate(optional_items, start=1):
        for current_capacity in range(remaining_capacity + 1):
            without_item = table[row - 1][current_capacity]
            with_item = -1
            if item.weight <= current_capacity:
                # 0-1 背包的“带”必须查上一行，保证每件物品最多使用一次。
                with_item = table[row - 1][current_capacity - item.weight] + item.value
            table[row][current_capacity] = max(without_item, with_item)

    selected_optional: list[Item] = []
    trace_reversed: list[BacktrackStep] = []
    current_capacity = remaining_capacity
    for row in range(len(optional_items), 0, -1):
        item = optional_items[row - 1]
        before = current_capacity
        if table[row][current_capacity] != table[row - 1][current_capacity]:
            selected_optional.append(item)
            current_capacity -= item.weight
            decision = "选择"
        else:
            decision = "不选"
        trace_reversed.append(BacktrackStep(item.name, decision, before, current_capacity))

    selected_names = {item.name for item in required_items + selected_optional}
    selected_items = [item for item in item_list if item.name in selected_names]
    required_trace: list[BacktrackStep] = []
    capacity_after_required = capacity
    for item in required_items:
        before = capacity_after_required
        capacity_after_required -= item.weight
        required_trace.append(BacktrackStep(item.name, "必选", before, capacity_after_required))
    trace = required_trace + trace_reversed

    return KnapsackResult(
        max_value=required_value + table[-1][-1],
        total_weight=sum(item.weight for item in selected_items),
        selected_items=selected_items,
        table=table,
        trace=trace,
        table_capacity=remaining_capacity,
    )


def sampled_last_row(result: KnapsackResult, step: int = 50) -> list[tuple[int, int]]:
    """按固定容量间隔提取 dp 表最后一行，便于写进报告。"""
    if step <= 0:
        raise ValueError("采样步长必须为正数")
    capacities = list(range(0, result.table_capacity + 1, step))
    if capacities[-1] != result.table_capacity:
        capacities.append(result.table_capacity)
    return [(capacity, result.table[-1][capacity]) for capacity in capacities]


if __name__ == "__main__":
    result = knapsack_01(DEFAULT_ITEMS, 1000)
    print(result.max_value, result.total_weight, [item.name for item in result.selected_items])
