from basic_strategy import simulate_games
from montecarlo_strategy import monte_carlo_policy_control
from collections import defaultdict
from montecarlo_strategy import calculate_hand_value, is_soft_hand, initialize_deck, draw_cards, play_dealer, get_hand_result, play_hand
import random


def calculate_win_rate(game_results):
    """计算玩家的胜率并返回详细统计"""
    player_wins = sum(result["result"] == "Player Wins!" for result in game_results)
    total_games = len(game_results)
    win_rate = player_wins / total_games
    return win_rate


def calculate_expected_return(game_results):
    """计算期望回报"""
    total_return = 0
    for result in game_results:
        if result["result"] == "Player Wins!":
            total_return += 1
        elif result["result"] == "Dealer Wins!":
            total_return -= 1
        # Tie 的回报为 0，无需处理

    expected_return = total_return / len(game_results)
    return expected_return

def simulate_with_policy(num_games, policy):
    """使用指定的策略进行模拟，返回游戏结果"""
    game_results = []
    for i in range(num_games):
        deck_id = initialize_deck()
        dealer_hand = draw_cards(deck_id, 2)
        player_hand = draw_cards(deck_id, 2)

        dealer_card = dealer_hand[0]['value']  # Dealer's visible card
        player_score = play_hand(deck_id, player_hand, policy)
        dealer_score = play_dealer(deck_id, dealer_hand)

        if player_score > 21:
            result = "Dealer Wins!"
        elif dealer_score > 21 or player_score > dealer_score:
            result = "Player Wins!"
        elif player_score < dealer_score:
            result = "Dealer Wins!"
        else:
            result = "Tie!"

        game_results.append({
            "game_id": i + 1,
            "player_score": player_score,
            "dealer_score": dealer_score,
            "result": result
        })

    return game_results


def iterative_optimization(num_iterations, num_games_per_iteration, epsilon=0.1):
    policy = None
    returns_sum = None
    returns_count = None

    for iteration in range(num_iterations):
        print(f"Iteration {iteration + 1}/{num_iterations}, Epsilon: {epsilon:.4f}")
        policy, returns_sum, returns_count = monte_carlo_policy_control(
            num_games=num_games_per_iteration,
            epsilon=epsilon,
            policy=policy,
            returns_sum=returns_sum,
            returns_count=returns_count
        )
        epsilon = max(0.1, epsilon * 0.99)  # 动态调整 epsilon

    return policy

if __name__ == '__main__':
    num_games = 1000  # 使用足够的模拟次数以获得稳定的结果
    num_iterations = 100  # 设置策略迭代的次数
    num_games_per_iteration = 1000  # 每次迭代中模拟的游戏数量

    # 1. 运行基本策略并评估
    basic_game_results, _ = simulate_games(num_games)  # 正确解包返回值
    basic_win_rate = calculate_win_rate(basic_game_results)
    basic_expected_return = calculate_expected_return(basic_game_results)

    print("Basic Strategy Results")
    print(f"Player Win Rate: {basic_win_rate:.2%}")
    print(f"Expected Return per Game: {basic_expected_return:.2f}\n")

    # 2. 运行蒙特卡洛策略控制算法并评估
    monte_carlo_policy, _, _ = monte_carlo_policy_control(num_games)
    monte_carlo_results = simulate_with_policy(num_games, monte_carlo_policy)
    monte_carlo_win_rate = calculate_win_rate(monte_carlo_results)
    monte_carlo_expected_return = calculate_expected_return(monte_carlo_results)

    print("Monte Carlo Strategy Results")
    print(f"Player Win Rate: {monte_carlo_win_rate:.2%}")
    print(f"Expected Return per Game: {monte_carlo_expected_return:.2f}\n")

    # 3. 运行迭代优化后的蒙特卡洛策略并评估
    optimal_policy = iterative_optimization(num_iterations, num_games_per_iteration)
    optimal_policy_results = simulate_with_policy(num_games, optimal_policy)
    optimal_policy_win_rate = calculate_win_rate(optimal_policy_results)
    optimal_policy_expected_return = calculate_expected_return(optimal_policy_results)

    print("Optimized Monte Carlo Strategy Results")
    print(f"Player Win Rate: {optimal_policy_win_rate:.2%}")
    print(f"Expected Return per Game: {optimal_policy_expected_return:.2f}\n")

    # 4. 对比结果
    print("Comparison of Strategies")
    print(f"Basic Strategy - Win Rate: {basic_win_rate:.2%}, Expected Return: {basic_expected_return:.2f}")
    print(f"Monte Carlo Strategy - Win Rate: {monte_carlo_win_rate:.2%}, Expected Return: {monte_carlo_expected_return:.2f}")
    print(f"Optimized Monte Carlo Strategy - Win Rate: {optimal_policy_win_rate:.2%}, Expected Return: {optimal_policy_expected_return:.2f}")
