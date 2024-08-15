import requests
import pandas as pd
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

    return aces_count > 0

def basic_strategy(player_total, dealer_card, is_soft, player_hand):
    if len(player_hand) == 2 and player_hand[0]['value'] == player_hand[1]['value']:
        if player_hand[0]['value'] in ['8', 'ACE']:
            return "Split"
        elif player_hand[0]['value'] in ['2', '3', '7']:
            return "Split" if dealer_card in ['2', '3', '4', '5', '6', '7'] else "Hit"
        elif player_hand[0]['value'] == '6':
            return "Split" if dealer_card in ['2', '3', '4', '5', '6'] else "Hit"
        elif player_hand[0]['value'] == '9':
            return "Split" if dealer_card not in ['7', '10', 'ACE'] else "Stand"
        elif player_hand[0]['value'] == '4':
            return "Split" if dealer_card in ['5', '6'] else "Hit"
        else:
            return "Stand"

    if is_soft:
        if player_total >= 19:
            return "Stand"
        elif player_total == 18:
            return "Stand" if dealer_card in ['2', '7', '8'] else "Hit"
        elif player_total == 17 or player_total == 16:
            return "Hit" if dealer_card in ['2', '3', '4', '7', '8', '9', '10', 'ACE'] else "Double"
        else:
            return "Hit"

    if player_total >= 17:
        return "Stand"
    elif player_total == 16:
        return "Stand" if dealer_card in ['2', '3', '4', '5', '6'] else "Hit"
    elif player_total == 15:
        return "Stand" if dealer_card in ['2', '3', '4', '5', '6'] else "Hit"
    elif player_total == 13 or player_total == 14:
        return "Stand" if dealer_card in ['2', '3', '4', '5', '6'] else "Hit"
    elif player_total == 12:
        return "Hit" if dealer_card in ['2', '3', '7', '8', '9', '10', 'ACE'] else "Stand"
    elif player_total == 11:
        return "Double"
    elif player_total == 10:
        return "Double" if dealer_card not in ['10', 'ACE'] else "Hit"
    elif player_total == 9:
        return "Double" if dealer_card in ['3', '4', '5', '6'] else "Hit"
    else:
        return "Hit"

def draw_cards(deck_id, count):
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}')
    return response.json()['cards']

def initialize_deck():
    response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
    return response.json()['deck_id']

def play_hand(deck_id, hand, dealer_card):
    while True:
        player_total = calculate_hand_value(hand)
        is_soft = is_soft_hand(hand)
        action = basic_strategy(player_total, dealer_card, is_soft, hand)
        
        if action == "Hit":
            card = draw_cards(deck_id, 1)[0]
            hand.append(card)
            if calculate_hand_value(hand) > 21:
                return "Busted", calculate_hand_value(hand)
        elif action == "Stand":
            return "Stand", calculate_hand_value(hand)
        elif action == "Double":
            card = draw_cards(deck_id, 1)[0]
            hand.append(card)
            return "Double", calculate_hand_value(hand)
        elif action == "Split":
            first_hand = [hand[0], draw_cards(deck_id, 1)[0]]
            return play_hand(deck_id, first_hand, dealer_card)

def play_dealer(deck_id, dealer_hand):
    dealer_score = calculate_hand_value(dealer_hand)
    while dealer_score < 17:
        card = draw_cards(deck_id, 1)[0]
        dealer_hand.append(card)
        dealer_score = calculate_hand_value(dealer_hand)
    
    
    return dealer_score

def simulate_games(num_games):
    game_results = []
    action_stats = {}

    dealer_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'ACE', 'JACK', 'QUEEN', 'KING']
    player_actions = ["Hit", "Stand", "Double", "Split"]
    for player_total in range(5, 22):
        action_stats[player_total] = {val: {action: 0 for action in player_actions} for val in dealer_values}

    for i in range(num_games):
        deck_id = initialize_deck()
        dealer_hand = draw_cards(deck_id, 2)
        player_hand = draw_cards(deck_id, 2)

        dealer_card = dealer_hand[0]['value']

        if dealer_card in ["JACK", "QUEEN", "KING"]:
            dealer_card = "10"

        dealer_card = str(dealer_card)

        player_total = calculate_hand_value(player_hand)
        is_soft = is_soft_hand(player_hand)

        if player_total < 5 or player_total > 21:
            continue

        player_action, player_score = play_hand(deck_id, player_hand, dealer_card)

        if player_action not in action_stats[player_total][dealer_card]:
            continue
        
        action_stats[player_total][dealer_card][player_action] += 1

        dealer_score = play_dealer(deck_id, dealer_hand)

        if dealer_score > 21:
            result = "Dealer Busted!"  # 庄家爆牌
        
        if player_action == "Busted":
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

    return game_results, action_stats

def determine_best_actions(action_stats):
    best_actions = {}
    for player_total, dealer_actions in action_stats.items():
        best_actions[player_total] = {}
        for dealer_card, actions in dealer_actions.items():
            best_action = max(actions, key=actions.get)
            best_actions[player_total][dealer_card] = best_action
    return best_actions

def plot_strategy_table(best_actions):
    df = pd.DataFrame(best_actions).T

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

    cell_colours = df.applymap(color_map).values

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.axis('tight')
    ax.axis('off')
    
    ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, cellColours=cell_colours, loc='center', cellLoc='center')
    
    plt.title("Blackjack Basic Strategy Table")
    plt.show()

    df.to_csv('blackjack_strategy_table.csv')

if __name__ == '__main__':
    num_games = 10000
    game_results, action_stats = simulate_games(num_games)
    best_actions = determine_best_actions(action_stats)
    plot_strategy_table(best_actions)
