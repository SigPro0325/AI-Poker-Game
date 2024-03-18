import random
from itertools import combinations
from collections import Counter 

class Card:
    ranks = '23456789TJQKA'
    suits = 'diamonds clubs hearts spades'.split()
    rank_order = {rank: i for i, rank in enumerate(ranks, 2)}
    unicode_suits = {
        'spades': '\u2660',   # ♠
        'diamonds': '\u2666', # ♦
        'clubs': '\u2663',    # ♣
        'hearts': '\u2665'    # ♥
    }

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit[0].upper()}"

    def __lt__(self, other):
        if Card.rank_order[self.rank] != Card.rank_order[other.rank]:
            return Card.rank_order[self.rank] < Card.rank_order[other.rank]
        return Card.suits.index(self.suit) < Card.suits.index(other.suit)

    def __str__(self):
        return f"{self.rank}{self.unicode_suits[self.suit]}"

def print_hand(cards):
    card_lines = ['', '', '', '', '']
    
    for card in cards:
        rank = card.rank if card.rank != '10' else 'T'
        suit = card.unicode_suits[card.suit]
        card_lines[0] += '┌─────┐ '
        card_lines[1] += f'│{rank:<2}   │ '
        card_lines[2] += f'│  {suit}  │ '
        card_lines[3] += f'│   {rank:>2}│ '
        card_lines[4] += '└─────┘ '

    card_lines = '\n'.join(card_lines)
    print(card_lines)

class Deck:
    ranks = '23456789TJQKA'
    suits = 'diamonds clubs hearts spades'.split()

    def __init__(self, deck_count=1):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks] * deck_count
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, count):
        if len(self.cards) < count:
            raise ValueError("Not enough cards in the deck to deal")
        return [self.cards.pop() for _ in range(count)]

    def reset(self):
        self.__init__(deck_count=len(self.cards) // len(self.ranks) // len(self.suits))

class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.is_ai = is_ai
        self.hand = []
        self.chips = 1000  # Starting chips
        self.current_bet = 0
        self.folded = False
        self.all_in = False
        self.total_winnings = 0
        self.action_history = []

    def record_action(self, round_name, action):
        self.action_history.append((round_name, action))

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def bet(self, amount):
        if amount > self.chips:
            raise ValueError("Not enough chips to bet this amount")
        self.chips -= amount
        self.current_bet += amount
        if self.chips == 0:
            self.all_in = True

    def call(self, amount_to_call):
        self.bet(min(amount_to_call, self.chips))

    def raise_bet(self, raise_amount):
        self.bet(raise_amount)

    def fold(self):
        self.folded = True
        self.hand = []

    def check(self):
        if self.current_bet > 0:
            raise ValueError("Cannot check, there is a bet already")

    def add_winnings(self, amount):
        self.total_winnings += amount

    def reset_for_new_hand(self):
        self.hand = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False

    def __str__(self):
        return f"{self.name} - Chips: {self.chips}, Current Bet: {self.current_bet}, Folded: {self.folded}, All-In: {self.all_in}"

class TexasHoldem:
    def __init__(self, num_human_players, num_ai_players):
        self.deck = Deck()
        self.players = [Player(f'Player {i + 1}') for i in range(num_human_players)]
        self.players += [Player(f'AI {i + 1}', is_ai=True) for i in range(num_ai_players)]
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.small_blind = 10
        self.big_blind = 20
        self.current_player_index = 0

    def start_game(self):
        self.deck.shuffle()
        self.deal_hole_cards()
        self.play_round("Pre-flop")

        # The "flop"
        self.deal_community_cards(3)
        self.play_round("Flop")

        # The "turn"
        self.deal_community_cards(1)
        self.play_round("Turn")

        # The "river"
        self.deal_community_cards(1)
        self.play_round("River")

        # Determines the winner
        self.showdown()

        # Resets for a new game
        self.reset_game()

    def deal_hole_cards(self):
        for player in self.players:
            player.receive_cards(self.deck.deal(2))

    def calculate_pot_odds(self, player):
        call_amount = self.current_bet - player.current_bet
        if call_amount == 0:
            return float('inf')  # Can't divide by zero, so returns a high value
        return self.pot / call_amount

    def deal_community_cards(self, count):
        self.community_cards.extend(self.deck.deal(count))

    def play_round(self, round_name):
        print(f"Starting {round_name} round")
        self.current_bet = self.big_blind if round_name == "Pre-flop" else 0
        self.betting_round()

    def betting_round(self):
        number_of_bets = 0
        while number_of_bets < len(self.players):
            player = self.players[self.current_player_index]
            if not player.folded:
                self.player_turn(player)
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            number_of_bets += 1

    def print_divider(self, title=None):
        if title:
            print(f"\n{'=' * 10} {title} {'=' * 10}\n")
        else:
            print("\n" + "=" * 30 + "\n")

    def print_community_cards(self):
        cards = " ".join(str(card) for card in self.community_cards)
        print(f"Community Cards: {cards}")

    def print_player_hands(self):
        for player in self.players:
            if not player.folded:
                hand = " ".join(str(card) for card in player.hand)
                print(f"{player.name} hand: {hand} - Chips: {player.chips}")

    def print_pot(self):
        print(f"Current pot: {self.pot} chips")



    def play_round(self, round_name):
        self.print_divider(round_name)
        self.current_bet = self.big_blind if round_name == "Pre-flop" else 0
        self.betting_round()
        self.print_community_cards()

    def player_turn(self, player):
        self.print_divider(f"{player.name}'s Turn")
        if not player.is_ai:
            self.print_player_hand(player)
            self.print_community_cards()
            self.print_pot()
            action = self.get_player_decision(player)  # Gets a decision from a real player
        else:
            action = self.ai_decision(player)

    def print_player_hand(self, player):
        hand = " ".join(str(card) for card in player.hand)
        print(f"Your hand: {hand}")
        print(f"Chips: {player.chips}")
        print(f"Current bet: {player.current_bet}")
        print(f"Pot: {self.pot}")

    def get_player_decision(self, player):
        self.print_player_hand(player)
        print("Actions: 'fold', 'check', 'call', 'raise'")
        action = input("Enter your action: ").strip().lower()
        print(f"{player.name}'s turn. Current bet: {self.current_bet}. Your chips: {player.chips}")
        print(f"Your hand: {[str(card) for card in player.hand]}")
        print(f"Community Cards: {[str(card) for card in self.community_cards]}")
        print(f"Your current bet: {player.current_bet}")
        print(f"Your chips: {player.chips}")
        
        while not self.validate_action(action, player):
            print("Invalid action. Please try again.")
            action = input("Enter your action: ").strip().lower()

        return action

    def is_royal_flush(self, hand):
        required_ranks = {'T', 'J', 'Q', 'K', 'A'}
        hand_ranks = {card.rank for card in hand}
        hand_suits = {card.suit for card in hand}

        return len(hand_suits) == 1 and required_ranks.issubset(hand_ranks)

    def deal_community_cards(self, count):
        self.community_cards.extend(self.deck.deal(count))
        self.print_divider(f"Dealing the {'Flop' if count == 3 else 'Turn' if count == 1 else 'River'}")
        self.print_community_cards()

    
    def print_community_cards(self):
        print("\nCommunity Cards:")
        print_hand(self.community_cards)

    def print_player_hand(self, player):
        print(f"\n{player.name}'s hand:")
        print_hand(player.hand)

    def analyze_betting_patterns(self):
        # Example: Count how often each player raises
        raise_counts = {player.name: sum(action == 'raise' for _, action in player.action_history)
                        for player in self.players if not player.is_ai}


#Example analysis in a very basic form. Analyses opponents raising action and determiens whether
        #the raising pattern is either aggresive or passive. It then stores this information for the
        #rest of the game 
        player_styles = {}
        for player in self.players:
            if not player.is_ai:
                raise_count = raise_counts[player.name]
                if raise_count > len(player.action_history) / 2:
                    player_styles[player.name] = "Aggressive"
                else:
                    player_styles[player.name] = "Passive"
        
        return player_styles

    def estimate_potential_strength(self, hand, community_cards):
    

        # Combine hand and community cards for analysis
        total_cards = hand + community_cards
        rank_counts = Counter(card.rank for card in total_cards)

        # Count outs for different types of hands
        outs = 0
        if len(community_cards) < 5:  # Only calculate potential if the hand can still improve
            # Calculate straight outs
            straight_outs = self.calculate_straight_outs(rank_counts, total_cards)
            outs += straight_outs

            # Calculate flush outs
            flush_outs = self.calculate_flush_outs(total_cards)
            outs += flush_outs

            # Pair to Three of a Kind, etc.
            for rank, count in rank_counts.items():
                if count == 2:  # Potential Three of a Kind
                    outs += 2  # Two more cards to potentially get a Three of a Kind
                elif count == 3:  # Potential Four of a Kind
                    outs += 1  # One more card to potentially get a Four of a Kind

        # Assigns a potential strength based on the number of outs
        potential_strength = outs * 10  # This is arbitrary, for example purposes

        return potential_strength

    def calculate_straight_outs(self, rank_counts, total_cards):
        # Converts ranks to numerical values and sort
        values = sorted([Card.rank_order[card.rank] for card in total_cards])
        
        # Adds low Ace for the wheel straight (A-2-3-4-5)
        if 14 in values:
            values.append(1)

        # Finds gaps in the sequence of ranks and determine if there's a straight draw
        gaps = [b - a for a, b in zip(values, values[1:]) if b - a > 1]
        num_gaps = len(gaps)

        if num_gaps == 0:
            # Already a straight or better
            return 0
        
        # Counts the outs based on the number of gaps and where they occur
        if num_gaps == 1:
            if gaps[0] == 2:
                # Ones gap of one rank (gutshot straight draw)
                return 4
            else:
                # Open-ended straight draw
                return 8
        elif num_gaps == 2:
            if gaps[0] == 2 and gaps[1] == 2:
                # Two gaps but potentially still an open-ended straight draw
                return 8
            else:
                # Double gutshot straight draw
                return 4 * num_gaps
        else:
            # No straight draw or too many missing cards for a draw
            return 0

    def is_four_of_a_kind(self, sorted_hand):
        # Checks for four cards of the same rank in the sorted hand
        rank_counts = Counter(card.rank for card in sorted_hand)
        return 4 in rank_counts.values()

    def is_full_house(self, sorted_hand):
        # Counts the cards of each rank
        rank_counts = Counter(card.rank for card in sorted_hand)
        # Checks if there is a three of a kind and a pair
        has_three_of_a_kind = 3 in rank_counts.values()
        has_pair = list(rank_counts.values()).count(2) >= 1
        return has_three_of_a_kind and has_pair

    def is_flush(self, sorted_hand):
        # Checks if all cards in the hand are of the same suit
        if len(sorted_hand) < 5:
            return False
        suits = [card.suit for card in sorted_hand]
        return all(suit == suits[0] for suit in suits)

    def is_straight_flush(self, sorted_hand):
        return self.is_straight(sorted_hand) and self.is_flush(sorted_hand)


    def is_straight(self, sorted_hand):
        if len(sorted_hand) < 5:
            return False
        # Converts ranks to numerical values, considering Ace both high and low
        values = [Card.rank_order[card.rank] for card in sorted_hand]
        if 14 in values:  # Ace
            values.append(1)  # Adding Ace as low value
        values = sorted(set(values))  # Remove duplicates and sort
        for i in range(len(values) - 4):
            if values[i + 4] - values[i] == 4:  # Check for 5 consecutive values
                return True
        return False


    def is_three_of_a_kind(self, sorted_hand):
        rank_counts = Counter(card.rank for card in sorted_hand)
        return 3 in rank_counts.values()

    def is_two_pair(self, sorted_hand):
        rank_counts = Counter(card.rank for card in sorted_hand)
        pairs = [rank for rank, count in rank_counts.items() if count == 2]
        return len(pairs) == 2


    def is_one_pair(self, sorted_hand):
        rank_counts = Counter(card.rank for card in sorted_hand)
        return 2 in rank_counts.values()

    def is_straight_flush(self, sorted_hand):
        # Checks if all cards are in sequence and of the same suit
        if len(sorted_hand) < 5:
            return False
        return (all(sorted_hand[i].suit == sorted_hand[0].suit for i in range(len(sorted_hand))) and
                all(Card.rank_order[sorted_hand[i].rank] == Card.rank_order[sorted_hand[i-1].rank] + 1 for i in range(1, len(sorted_hand))))



    def calculate_flush_outs(self, total_cards):
        """Calculate the number of outs for a flush draw."""
        suit_counts = Counter(card.suit for card in total_cards)
        # Finds the suit with the most cards in hand and on the table
        most_common_suit = suit_counts.most_common(1)
        
        if most_common_suit:
            num_cards_in_suit = most_common_suit[0][1]
            
            if num_cards_in_suit == 4:
                return 9
            elif num_cards_in_suit == 3 and len(total_cards) <= 5:
                return 1  
        return 0  

    # AI decision logic
    def ai_decision(self, player):
        hand_strength = self.evaluate_hand_strength(player.hand + self.community_cards)
        potential_strength = self.estimate_potential_strength(player.hand, self.community_cards)  # Corrected line
        pot_odds = self.calculate_pot_odds(player)
        player_styles = self.analyze_betting_patterns()

        # Example of simple betting pattern analysis
        aggressive_players = sum(p.current_bet > self.big_blind for p in self.players if not p.is_ai and not p.folded)

        # Bluffing - occasionally bluff with a weak hand
        if hand_strength < 500 and random.random() < 0.1:
            return f'raise {min(player.chips, self.big_blind * 2)}'  # Bluff with a raise

        # Deception - vary the strategy
        if random.random() < 0.2:
            return 'fold' if hand_strength > 1000 else 'call'  # Unexpected moves

        # Regular decision logic
        if hand_strength >= 1000 or potential_strength > 700:  # Strong hand or good potential
            if aggressive_players > 0:
                return 'call'  # Play cautiously against aggressive players
            else:
                return f'raise {min(player.chips, self.big_blind * 2)}'
        elif hand_strength >= 500:  
            if pot_odds > 1.5:
                return 'call'
            else:
                return 'fold'
        else:
            return 'fold'

    def evaluate_hand_strength(self, cards):
        best_hand_score = 0
        for hand in combinations(cards, 5):
            score = self.score_hand(hand)
            if score > best_hand_score:
                best_hand_score = score
        return best_hand_score

    def score_hand(self, hand):
        # Sorting the cards in descending order of rank for easier evaluation
        sorted_hand = sorted(hand, key=lambda card: Card.rank_order[card.rank], reverse=True)
        if self.is_royal_flush(sorted_hand):
            return 10000
        elif self.is_straight_flush(sorted_hand):
            return 9000 + self.rank_score(sorted_hand[0])
        elif self.is_four_of_a_kind(sorted_hand):
            return 8000 + self.rank_score(sorted_hand[2])  # The middle card in a sorted 4-of-a-kind is part of the quadruplet
        elif self.is_full_house(sorted_hand):
            return 7000 + self.rank_score(sorted_hand[2])  # The middle card in a sorted full house is part of the triplet
        elif self.is_flush(sorted_hand):
            return 6000 + self.high_card_score(sorted_hand)
        elif self.is_straight(sorted_hand):
            return 5000 + self.rank_score(sorted_hand[0])
        elif self.is_three_of_a_kind(sorted_hand):
            return 4000 + self.rank_score(sorted_hand[2])  # The middle card in a sorted 3-of-a-kind is part of the triplet
        elif self.is_two_pair(sorted_hand):
            return 3000 + self.high_pair_score(sorted_hand)
        elif self.is_one_pair(sorted_hand):
            return 2000 + self.pair_score(sorted_hand)
        else:
            return 1000 + self.high_card_score(sorted_hand)

    def rank_score(self, card):
        return Card.rank_order[card.rank]

    def high_card_score(self, hand):
        return sum(Card.rank_order[card.rank] for card in hand)

    def high_pair_score(self, hand):
        ranks = [card.rank for card in hand]
        pair_ranks = [rank for rank in set(ranks) if ranks.count(rank) == 2]
        return sum([self.rank_score(Card(rank, 'spades')) for rank in pair_ranks])  # Suit is irrelevant for scoring

    def pair_score(self, hand):
        ranks = [card.rank for card in hand]
        pair_rank = next(rank for rank in set(ranks) if ranks.count(rank) == 2)
        return self.rank_score(Card(pair_rank, 'spades'))  # Suit is irrelevant for scoring
    
    def player_turn(self, player):
        if player.is_ai:
            action = self.ai_decision(player)  # AI decision logic
        else:
            action = self.get_player_decision(player)  # Gets a decision from a real player

        if action == 'fold':
            player.fold()
            print(f"{player.name} folds.")
        elif action == 'check':
            player.check()
            print(f"{player.name} checks.")
        elif action == 'call':
            bet_amount = self.current_bet - player.current_bet
            player.call(bet_amount)
            self.pot += bet_amount
            print(f"{player.name} calls with {bet_amount} chips.")
        elif action.startswith('raise'):
            raise_amount = int(action.split()[1])
            player.raise_bet(raise_amount)
            self.current_bet = player.current_bet
            self.pot += raise_amount
            print(f"{player.name} raises by {raise_amount} chips.")
        else:
            raise ValueError("Invalid action")
            player.record_action(self.current_round_name, action)



    def validate_action(self, action, player):
        try:
            action_parts = action.split()
            action_type = action_parts[0]

            if action_type not in ['fold', 'check', 'call', 'raise']:
                return False
            if action_type == 'check' and self.current_bet > 0:
                return False
            if action_type == 'call' and (self.current_bet - player.current_bet) > player.chips:
                return False
            if action_type == 'raise':
                if len(action_parts) < 2:
                    print("Please specify an amount to raise.")
                    return False
                raise_amount = int(action_parts[1])
                if raise_amount <= 0 or raise_amount < self.big_blind or (raise_amount + self.current_bet) > player.chips:
                    print("Invalid raise amount.")
                    return False
            return True
        except ValueError:
            print("Please enter a valid number for raise amount.")
            return False
   

    def showdown(self):
        active_players = [p for p in self.players if not p.folded and not p.is_ai]
        if not active_players:
            # Handles case where all real players have folded
            # AI wins the pot
            pass
        else:
            # Evaluates hands of remaining players
            best_hand = None
            winning_player = None
            for player in active_players:
                player_hand = self.evaluate_hand(player.hand, self.community_cards)
                if not best_hand or self.compare_hands(player_hand, best_hand) > 0:
                    best_hand = player_hand
                    winning_player = player

            winning_player.add_winnings(self.pot)
            print(f"{winning_player.name} wins the pot of {self.pot} chips")

    def evaluate_hand(self, hand, community_cards):
        all_cards = hand + community_cards
        all_cards.sort(reverse=True)

        # Checks for each type of hand starting from the strongest
        if self.is_royal_flush(all_cards): return (10,)
        if self.is_straight_flush(all_cards): return (9, self.high_card_of_straight(all_cards))
        if self.is_four_of_a_kind(all_cards): return (8, self.four_of_a_kind_value(all_cards))
        if self.is_full_house(all_cards): return (7, self.full_house_values(all_cards))
        if self.is_flush(all_cards): return (6, self.flush_values(all_cards))
        if self.is_straight(all_cards): return (5, self.high_card_of_straight(all_cards))
        if self.is_three_of_a_kind(all_cards): return (4, self.three_of_a_kind_value(all_cards))
        if self.is_two_pair(all_cards): return (3, self.two_pair_values(all_cards))
        if self.is_one_pair(all_cards): return (2, self.one_pair_value(all_cards))
        return (1, self.high_cards(all_cards))


    def compare_hands(self, hand1, hand2):
        if hand1[0] != hand2[0]:
            return hand1[0] - hand2[0]

        # If hand ranks are equal, compares the high cards or tiebreakers
        return self.compare_high_cards(hand1[1:], hand2[1:])

    def compare_high_cards(self, cards1, cards2):
        for c1, c2 in zip(cards1, cards2):
            if c1 != c2:
                return c1 - c2
        return 0  # Hands are exactly equal

    def reset_game(self):
        # Reset the game state for a new hand
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.current_player_index = (self.current_player_index + 1) % len(self.players)  # Small blind moves to the next player
        for player in self.players:
            player.reset_for_new_hand()

# Example usage
num_human_players = int(input("How many human players will play? "))
num_ai_players = int(input("How many AI players will play? "))
game = TexasHoldem(num_human_players, num_ai_players)
game.start_game()
