# Optimal strategy of Blackjack with Monte Carlo method

## Overview  
A Blackjack game written in React.js which can be found from [Blackjack Game](https://blackjack-simulator.onrender.com). This project focuses on optimizing the strategy for playing Blackjack using Monte Carlo simulations. Blackjack is a popular card game where the goal is to get a hand value as close to 21 as possible without exceeding it. The project aims to develop and compare different strategies, including a basic strategy and an optimized strategy using Monte Carlo methods.

## Visualize the Game
![](src/blackjack-screenshot.jpg)

## Features
- **Basic Strategy Implementation**: A straightforward strategy that mimics standard Blackjack playing techniques.
- **Monte Carlo Simulation**: A method to optimize the Blackjack strategy by simulating thousands of games and adjusting the strategy based on observed outcomes.
- **Win Rate and Expected Return Analysis**: Compare the effectiveness of the basic strategy and the Monte Carlo-optimized strategy by calculating the win rate and expected return.

## Directory Structure
project/  
│  
├── basic_strategy.py # Implementation of the basic Blackjack strategy  
├── montecarlo_strategy.py # Implementation of the Monte Carlo strategy and simulation  
├── iterative_optimization.py # Code for iterative optimization of the strategy  
├── README.md # Project documentation  
├── requirements.txt # List of dependencies  
└── data/ # Directory for storing any generated data or results


### Getting started
To run the project locally, you'll need to have Python installed. Follow these steps to set up the environment:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ZixuanGao23206703/BlackJack-Simulator.git
    cd BlackJack-simulator
    ```

2. **Create a Virtual Environment** :
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
## Usage

### Running the Basic Strategy

To simulate games using the basic strategy, run:

```bash
python basic_strategy.py
```
### Running the Monte Carlo Simulation
To optimize and simulate the strategy using Monte Carlo methods, run:
```bash
python montecarlo_strategy.py
```
### Iterative Strategy Optimization
For a deeper optimization that involves multiple iterations:

```bash
python iterative_optimization.py
```
This script will run several iterations of the Monte Carlo simulation, further refining the strategy with each iteration.

## Results
After running the simulations, you will find the optimized strategy printed in the console, showing which actions to take in different scenarios (e.g., when the player's sum is 16 and the hand is soft). Additionally, win rates and expected returns are displayed for both the basic and optimized strategies.

## Project Goals
- **Understanding Basic and Optimized Strategies**: Learn the differences between a basic strategy and an optimized strategy in Blackjack.
- **Strategy Improvement**: Demonstrate how Monte Carlo simulations can be used to improve decision-making in uncertain environments like card games.
- **Practical Application**: Provide a framework that can be adapted to other decision-making problems or games.

## Future Work
- **Reinforcement Learning Integration**: Explore the possibility of using reinforcement learning to further optimize the strategy.
- **Extend to Multi-Deck Games**: Modify the simulation to handle more complex variations of Blackjack with multiple decks.
- **UI Development&**: Develop a simple GUI to make the simulation accessible to non-programmers.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


### Contact  
Developer: Zixuan Gao               
LinkedIn: https://www.linkedin.com/in/zixuan-gia/   
GitHub: https://github.com/ZixuanGao23206703




