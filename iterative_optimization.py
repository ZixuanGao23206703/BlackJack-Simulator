from montecarlo_strategy import monte_carlo_policy_control
import matplotlib.pyplot as plt
import pandas as pd

def iterative_optimization(num_iterations, num_games_per_iteration, epsilon=0.5):  # 更高的初始 epsilon 值
    policy = None
    returns_sum = None
    returns_count = None

    for iteration in range(num_iterations):
        print(f"Iteration {iteration + 1}/{num_iterations}")
        policy, returns_sum, returns_count = monte_carlo_policy_control(
            num_games=num_games_per_iteration,
            epsilon=epsilon,
            policy=policy,
            returns_sum=returns_sum,
            returns_count=returns_count
        )

        # Observe the policy evolution
        if iteration > 0 and iteration % 5 == 0:
            print(f"Sample policy after {iteration + 1} iterations:")
            for player_sum in range(15, 22):
                state_hard = (player_sum, "10", False)  # 硬手，庄家明牌为10
                state_soft = (player_sum, "10", True)   # 软手，庄家明牌为10

                if state_hard in policy:
                    print(f"Player sum {player_sum} (hard): {policy[state_hard]}")
                elif state_soft in policy:
                    print(f"Player sum {player_sum} (soft): {policy[state_soft]}")
                else:
                    print(f"Player sum {player_sum}: No policy found")
        
        # 动态调整 epsilon，逐步减少随机性，增加收敛性
        epsilon = max(0.1, epsilon * 0.995)  # 更慢的 epsilon 衰减

    return policy

import pandas as pd
import matplotlib.pyplot as plt

def plot_strategy_table(policy):
    # 创建 DataFrame，df 只在这个函数内部使用
    df = pd.DataFrame(index=range(5, 22), columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'ACE', 'JACK', 'QUEEN', 'KING'])

    print("Plotting strategy table...")  # 调试信息
    print("Current policy states:", list(policy.keys())[:10])  # 打印前10个状态

    for player_sum in range(5, 22):
        for dealer_card in df.columns:
            # 在这里我们要用与 monte_carlo_policy_control 相同的 state 定义
            state_hard = (player_sum, dealer_card, False)  # 硬手状态
            state_soft = (player_sum, dealer_card, True)   # 软手状态
            
            if state_hard in policy:
                df.at[player_sum, dealer_card] = policy[state_hard]
            elif state_soft in policy:
                df.at[player_sum, dealer_card] = policy[state_soft]
            else:
                df.at[player_sum, dealer_card] = 'N/A'

    # 使用颜色编码来区分动作
    def color_map(val):
        if val == 'Stand':
            return 'yellow'
        elif val == 'Hit':
            return 'red'
        elif val == 'Double':
            return 'blue'
        elif val == 'Split':
            return 'green'
        else:
            return 'white'

    # 映射颜色
    cell_colours = df.applymap(color_map).values

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    
    ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, cellColours=cell_colours, loc='center', cellLoc='center')

    plt.title("Blackjack Optimal Strategy Table (Monte Carlo)")
    plt.show()

    df.to_csv('blackjack_optimal_strategy_table.csv')  # 保存为CSV

# 主程序
if __name__ == '__main__':
    num_iterations = 100  # 设置策略迭代的次数
    num_games_per_iteration = 1000  # 每次迭代中模拟的游戏数量

    optimal_policy = iterative_optimization(num_iterations, num_games_per_iteration)

    # 调用 plot_strategy_table 函数，绘制策略表
    plot_strategy_table(optimal_policy)

    # example 输出
    for player_sum in range(15, 22):
        state_hard = (player_sum, "10", False)  # 硬手示例
        state_soft = (player_sum, "10", True)   # 软手示例

        if state_hard in optimal_policy:
            print(f"Player sum {player_sum} (hard): {optimal_policy[state_hard]}")
        elif state_soft in optimal_policy:
            print(f"Player sum {player_sum} (soft): {optimal_policy[state_soft]}")
        else:
            print(f"Player sum {player_sum}: No policy found")

