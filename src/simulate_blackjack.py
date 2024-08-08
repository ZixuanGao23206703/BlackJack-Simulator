import requests
import pandas as pd

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
        return 'Player Busted!'
    elif dealer_total > 21:
        return 'Player Wins!'
    elif player_total > dealer_total:
        return 'Player Wins!'
    elif player_total < dealer_total:
        return 'Dealer Wins!'
    else:
        return 'Tie!'

def draw_cards(deck_id, count):
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}')
    return response.json()['cards']

def initialize_deck():
    response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
    return response.json()['deck_id']

def play_hand(deck_id, hand):
    results = []
    score = calculate_hand_value(hand)
    initial_hard = not is_soft_hand(hand)
    res = {
        "score": score,  # Player's initial score
        "score_dealer": None,
        "hard": initial_hard,
        "score_if_hit": score,
        "score_fin_dealer": None,
        "hit": 0,
        "stand": 1,
        "hard_if_hit": initial_hard,
        "result": None
    }

    while res["score_if_hit"] < 17:
        card = draw_cards(deck_id, 1)[0]
        hand.append(card)
        res["score_if_hit"] = calculate_hand_value(hand)
        res["hard_if_hit"] = not is_soft_hand(hand)
        res["hit"] = 1
        res["stand"] = 0
        results.append(res.copy())

        res = {
            "score": res["score"],  # Player's initial score
            "score_dealer": None,
            "hard": res["hard_if_hit"],
            "score_if_hit": res["score_if_hit"],
            "score_fin_dealer": None,
            "hit": 0,
            "stand": 1,
            "hard_if_hit": res["hard_if_hit"],
            "result": None
        }

        if res["score_if_hit"] >= 21:
            break

    if not results:
        results.append(res)
    else:
        results[-1]["stand"] = 1

    return results

def play_dealer(deck_id, dealer_hand):
    dealer_score = calculate_hand_value(dealer_hand)
    while dealer_score < 17:
        card = draw_cards(deck_id, 1)[0]
        dealer_hand.append(card)
        dealer_score = calculate_hand_value(dealer_hand)
    return dealer_score

def simulate_games(num_games):
    game_results = []

    for i in range(num_games):
        deck_id = initialize_deck()
        dealer_hand = draw_cards(deck_id, 2)
        player_hand = draw_cards(deck_id, 2)

        game_id = i + 1
        player_score = calculate_hand_value(player_hand)  # Player's initial score
        dealer_score = calculate_hand_value(dealer_hand)  # Dealer's initial score

        player_results = play_hand(deck_id, player_hand)
        final_dealer_score = play_dealer(deck_id, dealer_hand)

        for res in player_results:
            res["score_dealer"] = dealer_score  # Dealer's initial score
            res["score_fin_dealer"] = final_dealer_score
            res["result"] = get_hand_result(res["score_if_hit"], final_dealer_score)
            res["game_id"] = game_id

        game_results.extend(player_results)

    return game_results

if __name__ == '__main__':
    num_games = 10
    game_results = simulate_games(num_games)

    
    df = pd.DataFrame(game_results)
    df.to_csv('gameData.csv', index=False)

    print(df.head())
