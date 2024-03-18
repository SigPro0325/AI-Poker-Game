# AI-Poker-Game
Texas Hold'em Poker Simulator 

This Texas Hold'em Poker Simulator is a comprehensive Python application designed to simulate the popular poker game for both human and AI players. The simulation includes a deck of cards, player management, betting rounds, and the evaluation of poker hands, providing an interactive and customizable poker game experience. Whether you're practicing your poker strategy, learning the game, or just looking for some fun, this simulator offers a deep dive into the mechanics of Texas Hold'em.

## Features

- **Customizable Game Setup**: Choose the number of human and AI players to tailor the game experience.
- **Automated Deck Management**: The deck is automatically shuffled, and cards are dealt at the beginning of each game and round.
- **Betting Rounds**: Supports all standard betting rounds in Texas Hold'em, including pre-flop, flop, turn, and river.
- **Dynamic Hand Evaluation**: Automatically evaluates the strength of each hand, determining winners based on standard poker hand rankings.
- **AI Players**: Simple AI behavior for non-human players, making decisions based on hand strength and potential.

## Classes and Methods

- `Card`: Represents a single playing card, providing utilities for card comparison and display.
- `Deck`: Manages a deck of cards, supporting shuffling and dealing.
- `Player`: Represents a player, tracking chips, bets, and actions.
- `TexasHoldem`: Coordinates the game flow, managing players, community cards, and the pot.

## Usage

To start a game, simply run the script and follow the prompts to set the number of human and AI players. The game will guide you through each betting round, displaying cards, and managing bets until a winner is determined.

### Example

```python
num_human_players = int(input("How many human players will play? "))
num_ai_players = int(input("How many AI players will play? "))
game = TexasHoldem(num_human_players, num_ai_players)
game.start_game()

Dependencies
Python 3.x
No external libraries required.
Note
This simulator is intended for educational and entertainment purposes only. It simulates a basic version of Texas Hold'em poker and includes simple AI for non-human players. The AI logic is basic and meant to demonstrate the potential for further development.

Contributing
Contributions, issues, and feature requests are welcome! Feel free to fork the repository and submit pull requests with your improvements.

