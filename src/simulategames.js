import axios from 'axios';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { dirname } from 'path';


const calculateHandValue = (hand) => {
  let total = 0;
  let acesCount = 0;

  hand.forEach(card => {
    const values = {
      ACE: 11,
      KING: 10,
      QUEEN: 10,
      JACK: 10
    };
    total += (values[card.value] || parseInt(card.value, 10));
    if (card.value === 'ACE') acesCount++;
  });

  while (total > 21 && acesCount > 0) {
    total -= 10;
    acesCount--;
  }

  return total;
};

const isSoftHand = (hand) => {
  let total = 0;
  let acesCount = 0;

  hand.forEach(card => {
    if (card.value === 'ACE') {
      acesCount++;
      total += 11;
    } else {
      const values = {
        KING: 10,
        QUEEN: 10,
        JACK: 10
      };
      total += (values[card.value] || parseInt(card.value, 10));
    }
  });

  while (total > 21 && acesCount > 0) {
    total -= 10;
    acesCount--;
  }

  return total <= 21 && acesCount > 0;
};


const getHandResult = (playerTotal, dealerTotal) => {
  if (playerTotal > 21) {
    return 'Player Busted!';
  } else if (dealerTotal > 21) {
    return 'Player Wins!';
  } else if (playerTotal > dealerTotal) {
    return 'Player Wins!';
  } else if (playerTotal < dealerTotal) {
    return 'Dealer Wins!';
  } else {
    return 'Tie!';
  }
};

const simulateGames = async (numGames) => {
  const gameResults = [];

  const initializeDeck = async () => {
    const response = await axios.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1');
    return response.data.deck_id;
  };

  const getCard = async (deck_id) => {
    const response = await axios.get(`https://deckofcardsapi.com/api/deck/${deck_id}/draw/?count=1`);
    if (response.data.cards.length === 0) {
      throw new Error('No more cards in the deck');
    }
    return response.data.cards[0];
  };

  const playHand = async (deck_id, hand) => {
    let score = calculateHandValue(hand);
    const initialHard = !isSoftHand(hand);
    let result = [];
    let res = {
      score: score,
      score_dealer: null,
      hard: initialHard,
      score_if_hit: score, 
      score_fin_dealer: null,
      hit: 0,
      stand: 1, 
      hard_if_hit: initialHard,
      result: null
    };

    while (score < 17) { 
      const card = await getCard(deck_id);
      hand.push(card);
      score = calculateHandValue(hand);
      res.score_if_hit = score;
      res.hard_if_hit = !isSoftHand(hand);
      res.hit = 1;
      res.stand = 0; 
      result.push({ ...res });

      res = {
        score: score,
        score_dealer: null,
        hard: !isSoftHand(hand),
        score_if_hit: score,
        score_fin_dealer: null,
        hit: 0,
        stand: 1,
        hard_if_hit: null,
        result: null
      };

      if (score >= 21) break;
    }

    if (result.length === 0) {
      result.push(res);
    } else {
      result[result.length - 1].stand = 1;
    }

    return result;
  };

  const playDealer = async (deck_id, dealerHand) => {
    let dealerScore = calculateHandValue(dealerHand);
    while (dealerScore < 17) {
      const card = await getCard(deck_id);
      dealerHand.push(card);
      dealerScore = calculateHandValue(dealerHand);
    }
    return dealerScore;
  };

  for (let i = 0; i < numGames; i++) {
    const deck_id = await initializeDeck(); 
    let dealerHand = [];
    let playerHand = [];

  
    playerHand.push(await getCard(deck_id)); 
    dealerHand.push(await getCard(deck_id)); 
    playerHand.push(await getCard(deck_id)); 
    dealerHand.push(await getCard(deck_id)); 

 
    let playerScore = calculateHandValue(playerHand);
    let dealerScore = calculateHandValue(dealerHand);

    let game_id = i + 1;

    
    let playerResults = await playHand(deck_id, playerHand);

    
    let finalDealerScore = await playDealer(deck_id, dealerHand);
    
    playerResults.forEach(res => {
      res.score_dealer = dealerScore;
      res.score_fin_dealer = finalDealerScore;
      res.result = getHandResult(res.score_if_hit, finalDealerScore);
      res.game_id = game_id;
    });

    gameResults.push(...playerResults);
  }

  
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = dirname(__filename);

  
  fs.writeFileSync(`${__dirname}/gameData.json`, JSON.stringify(gameResults, null, 2), 'utf-8');
};


simulateGames(1000);
