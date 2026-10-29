# 独立研究任务

## 1 回溯法与 n 皇后问题

n 皇后问题要求在一个 `n × n` 棋盘上放置 `n` 个皇后，使任意两个皇后都不在同一行、同一列或同一条对角线上。

回溯法可以逐行放置皇后。每一行尝试一个列位置；如果新皇后与前面已经放好的皇后冲突，就立即撤销这一步并尝试下一列。它本质上是对“部分解树”进行深度优先搜索，并在发现当前选择不可能形成合法完整解时剪枝。

它与动态规划式穷举的主要区别是：

- 回溯法保存当前选择路径，发现违反约束就退回；它通常不会保存并复用已经算过的子问题。
- 动态规划先定义状态，把重复出现的相同子问题合并并保存结果；以后再次遇到该状态时直接查表。
- 因此，回溯依靠“约束剪枝”减少搜索，动态规划依靠“重叠子问题和记忆”避免重复计算。n 皇后最自然的解法是回溯；如果只统计方案数，也可以把列和对角线占用情况编码成状态再记忆化。

## 2 完全背包需要修改哪一行

0-1 背包中“选择第 i 件物品”的递推是：

```text
dp[i][c] = dp[i-1][c-w[i]] + v[i]
```

完全背包允许第 `i` 件物品重复选择，因此应把右侧的上一行 `i-1` 改为当前行 `i`：

```text
dp[i][c] = dp[i][c-w[i]] + v[i]
```

完整递推为：

```text
dp[i][c] = max(dp[i-1][c], dp[i][c-w[i]] + v[i])
```

如果使用一维数组，等价变化是：0-1 背包的容量循环从大到小，完全背包的容量循环从小到大，使同一件物品在本轮可以再次贡献。

## 3 分支限界法

一句话：分支限界法把候选解分成若干分支，并用每个分支可能达到的最好界限判断它是否还有机会超过当前最优解；没有机会的分支直接丢弃。

它比普通回溯更适合优化问题的地方是：回溯通常在部分解已经违反约束时才剪枝，而分支限界即使面对仍然可行的部分解，也能因其“理论最好结果仍不够好”而提前剪掉。不过它不保证总是更快；如果界限很松，仍可能接近遍历整个搜索空间。

## 资料来源

- 课程第 6 次课课件及实践指南：https://aip-2026f.dev-learn-hub.me/a6
- NIST Dictionary of Algorithms and Data Structures，n queens：https://xlinux.nist.gov/dads/HTML/nqueens.html
- NIST Dictionary of Algorithms and Data Structures，backtracking：https://xlinux.nist.gov/dads/HTML/backtrack.html
- NIST Dictionary of Algorithms and Data Structures，branch and bound：https://xlinux.nist.gov/dads/HTML/branchNbound.html
- University of Maryland CMSC 451 讲义，0-1 Knapsack：https://www.cs.umd.edu/class/spring2025/cmsc451-0101/Lects/cmsc451-spring25-lects.pdf
- Land, A. H. and Doig, A. G. (1960). *An Automatic Method of Solving Discrete Programming Problems*. Econometrica, 28(3), 497–520. https://doi.org/10.2307/1910129
