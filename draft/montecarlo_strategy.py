import requests
import pandas as pd
from collections import defaultdict
import random
import matplotlib.pyplot as plt

def calculate_hand_value(hand):
    total = 0
    aces_count = 0

    values = {
        "ACE": 11,
        "KING": 10,
        "QUEEN": 10,
        "JACK": 10
    }

    for card in hand:
        if card['value'] in values:
            total += values[card['value']]
        else:
            total += int(card['value'])
        if card['value'] == 'ACE':
            aces_count += 1

    while total > 21 and aces_count > 0:
        total -= 10
        aces_count -= 1

    return total

def is_soft_hand(hand):
    total = 0
    aces_count = 0

    values = {
        "ACE": 11,
        "KING": 10,
        "QUEEN": 10,
        "JACK": 10
    }

    for card in hand:
        if card['value'] == 'ACE':
            aces_count += 1
            total += 11
        else:
            total += values.get(card['value'], int(card['value']) if card['value'].isdigit() else 0)

    while total > 21 and aces_count > 0:
        total -= 10
        aces_count -= 1

    return total <= 21 and aces_count > 0

def get_hand_result(player_total, dealer_total):
    if player_total > 21:
        return -1  # Player Busted, loss
    elif dealer_total > 21:
        return 1  # Dealer Busted, player wins
    elif player_total > dealer_total:
        return 1  # Player wins
    elif player_total < dealer_total:
        return -1  # Dealer wins
    else:
        return 0  # Tie

def draw_cards(deck_id, count):
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}')
    return response.json()['cards']

def initialize_deck():
    response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
    return response.json()['deck_id']

def play_hand(deck_id, hand, policy):
    score = calculate_hand_value(hand)
    initial_hard = not is_soft_hand(hand)

    while True:
        action = policy[(score, initial_hard)]  # 从策略中获取当前状态下的动作
        if action == 'Stand':
            break

        if action == 'Split' and len(hand) == 2 and hand[0]['value'] == hand[1]['value'] and score % 2 == 0:
            # 处理分牌操作
            hand1 = [hand[0], draw_cards(deck_id, 1)[0]]
            hand2 = [hand[1], draw_cards(deck_id, 1)[0]]
            score1 = play_hand(deck_id, hand1, policy)
            score2 = play_hand(deck_id, hand2, policy)
            return max(score1, score2)  # 返回较好的得分
        
        if action == 'Double':
            card = draw_cards(deck_id, 1)[0]
            hand.append(card)
            score = calculate_hand_value(hand)
            return score  # Double后直接结束玩家回合

        card = draw_cards(deck_id, 1)[0]
        hand.append(card)
        score = calculate_hand_value(hand)
        initial_hard = not is_soft_hand(hand)

        if score >= 21:
            break

    return score




def play_dealer(deck_id, dealer_hand):
    dealer_score = calculate_hand_value(dealer_hand)
    while dealer_score < 17:
        card = draw_cards(deck_id, 1)[0]
        dealer_hand.append(card)
        dealer_score = calculate_hand_value(dealer_hand)
    return dealer_score

def monte_carlo_policy_control(num_games, epsilon=0.2, policy=None, returns_sum=None, returns_count=None):
    actions = ['Hit', 'Stand', 'Double', 'Split']

    if policy is None:
        policy = defaultdict(lambda: random.choice(actions))  # 初始策略：随机选择
    if returns_sum is None:
        returns_sum = defaultdict(float)
    if returns_count is None:
        returns_count = defaultdict(float)

    for i in range(num_games):
        deck_id = initialize_deck()
        dealer_hand = draw_cards(deck_id, 2)
        player_hand = draw_cards(deck_id, 2)

        dealer_card = dealer_hand[0]['value']
        if dealer_card in ["JACK", "QUEEN", "KING"]:
            dealer_card = "10"

        episode = []
        final_score = None

        while True:
            score = calculate_hand_value(player_hand)
            state = (score, dealer_card, is_soft_hand(player_hand))

            if score >= 21:
                action = 'Stand'
            else:
                if random.random() > epsilon:
                    action = policy[state]
                else:
                    action = random.choice(actions)

            # 添加防止 Split 出现在不合理情况下的逻辑
            if action == 'Split' and (len(player_hand) != 2 or player_hand[0]['value'] != player_hand[1]['value']):
                action = 'Hit'  # 如果不符合 Split 条件，默认改为 Hit

            episode.append((state, action))

            if action == 'Stand':
                final_score = calculate_hand_value(player_hand)
                break
            elif action == 'Double':
                card = draw_cards(deck_id, 1)[0]
                player_hand.append(card)
                final_score = calculate_hand_value(player_hand)
                break
            elif action == 'Split':
                hand1 = [player_hand[0], draw_cards(deck_id, 1)[0]]
                hand2 = [player_hand[1], draw_cards(deck_id, 1)[0]]
                final_score = max(play_hand(deck_id, hand1, policy), play_hand(deck_id, hand2, policy))
                break
            else:  # Hit
                card = draw_cards(deck_id, 1)[0]
                player_hand.append(card)
                final_score = calculate_hand_value(player_hand)
                if final_score >= 21:
                    break

        if final_score is None:
            final_score = calculate_hand_value(player_hand)

        final_dealer_score = play_dealer(deck_id, dealer_hand)
        reward = get_hand_result(final_score, final_dealer_score)

        for state, action in episode:
            sa_pair = (state, action)
            returns_sum[sa_pair] += reward
            returns_count[sa_pair] += 1.0
            avg_return = returns_sum[sa_pair] / returns_count[sa_pair]

            best_action = max(actions, key=lambda a: returns_sum[(state, a)] / returns_count[(state, a)] if returns_count[(state, a)] > 0 else float('-inf'))

            # 在更新策略时再次检查 Split 条件
            if best_action == 'Split' and (state[0] % 2 != 0 or state[0] < 4):
                best_action = 'Hit'

            policy[state] = best_action

    return policy, returns_sum, returns_count




def plot_strategy_table(policy):
    df = pd.DataFrame(index=range(5, 22), columns=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'ACE', 'JACK', 'QUEEN', 'KING'])

    for player_sum in range(5, 22):
        for dealer_card in df.columns:
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

    plt.title("Blackjack Montecarlo Strategy Table")
    plt.show()

    df.to_csv('blackjack_montecarlo_strategy_table.csv')  # 保存为CSV


if __name__ == '__main__':
    num_games = 10000
    optimal_policy, _, _ = monte_carlo_policy_control(num_games)

    plot_strategy_table(optimal_policy)

    # example
    for player_sum in range(15, 22):
        state_hard = (player_sum, "10", False)  # 示例：硬手，庄家明牌为10
        state_soft = (player_sum, "10", True)   # 示例：软手，庄家明牌为10

        if state_hard in optimal_policy:
            print(f"Player sum {player_sum} (hard): {optimal_policy[state_hard]}")
        elif state_soft in optimal_policy:
            print(f"Player sum {player_sum} (soft): {optimal_policy[state_soft]}")
        else:
            print(f"Player sum {player_sum}: No policy found")

