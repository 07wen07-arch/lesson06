"""只用 Python 标准库执行的自动化验收测试。"""

from __future__ import annotations

import itertools
import unittest

from coin_change import coin_dp, coin_greedy
from knapsack import DEFAULT_ITEMS, Item, knapsack_01


def brute_force(
    items: list[Item], capacity: int, required_names: set[str] | None = None
) -> tuple[int, set[str]]:
    """枚举小数据的所有组合，用独立方法核验动态规划结果。"""
    required_names = required_names or set()
    best_value = -1
    best_names: set[str] = set()
    for flags in itertools.product((False, True), repeat=len(items)):
        chosen = [item for item, flag in zip(items, flags) if flag]
        names = {item.name for item in chosen}
        weight = sum(item.weight for item in chosen)
        value = sum(item.value for item in chosen)
        if required_names <= names and weight <= capacity and value > best_value:
            best_value = value
            best_names = names
    return best_value, best_names


class CoinChangeTests(unittest.TestCase):
    def test_greedy_checkpoint(self) -> None:
        self.assertEqual(coin_greedy([1, 5, 11], 15), (5, [11, 1, 1, 1, 1]))

    def test_dp_checkpoint(self) -> None:
        self.assertEqual(coin_dp([1, 5, 11], 15), (3, [5, 5, 5]))

    def test_unreachable_amount(self) -> None:
        with self.assertRaises(ValueError):
            coin_dp([4, 6], 3)


class KnapsackTests(unittest.TestCase):
    def assert_result_matches_bruteforce(
        self, capacity: int, required_names: set[str] | None = None
    ) -> None:
        required_names = required_names or set()
        result = knapsack_01(DEFAULT_ITEMS, capacity, required_names)
        brute_value, _ = brute_force(DEFAULT_ITEMS, capacity, required_names)
        self.assertEqual(result.max_value, brute_value)
        self.assertLessEqual(result.total_weight, capacity)
        self.assertTrue(required_names <= {item.name for item in result.selected_items})

    def test_standard_checkpoint(self) -> None:
        result = knapsack_01(DEFAULT_ITEMS, 1000)
        self.assertEqual(result.max_value, 315)
        self.assertEqual(result.total_weight, 1000)
        self.assertEqual([item.name for item in result.selected_items], ["睡袋", "食物", "水具"])

    def test_capacity_800(self) -> None:
        result = knapsack_01(DEFAULT_ITEMS, 800)
        self.assertEqual(result.max_value, 255)
        self.assertEqual(result.total_weight, 800)
        self.assertEqual([item.name for item in result.selected_items], ["炉具", "睡袋", "水具"])

    def test_required_item(self) -> None:
        result = knapsack_01(DEFAULT_ITEMS, 1000, {"炉具"})
        self.assertEqual(result.max_value, 295)
        self.assertEqual(result.total_weight, 950)
        self.assertEqual([item.name for item in result.selected_items], ["炉具", "睡袋", "食物"])

    def test_dp_matches_bruteforce_at_sampled_capacities(self) -> None:
        for capacity in range(0, 1001, 50):
            with self.subTest(capacity=capacity):
                self.assert_result_matches_bruteforce(capacity)

    def test_required_item_matches_bruteforce(self) -> None:
        for required in ({"帐篷"}, {"炉具"}, {"睡袋"}, {"食物"}, {"水具"}):
            with self.subTest(required=required):
                self.assert_result_matches_bruteforce(1000, required)


if __name__ == "__main__":
    unittest.main(verbosity=2)
