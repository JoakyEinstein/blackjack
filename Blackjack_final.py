
import random

# Card & Deck

def create_deck():
    """Create a standard Blackjack deck as a list of (rank, value) tuples."""
    ranks = [('A', 11)] + [(str(n), n) for n in range(2, 11)] + [('J', 10), ('Q', 10), ('K', 10)]
    deck = []
    for rank, value in ranks:
        for _ in range(4):  # four suits
            deck.append((rank, value))
    return deck


def shuffle_deck(deck):
    random.shuffle(deck)


def draw_card(deck):
    return deck.pop()


def initial_deal(deck):
    player_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]
    return player_hand, dealer_hand


# Hand Logic
def calculate_hand_value(hand):
    total = 0
    aces = 0
    for rank, value in hand:
        total += value
        if rank == 'A':
            aces += 1
    # Adjust for aces
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total


def is_blackjack(hand):
    return len(hand) == 2 and calculate_hand_value(hand) == 21


# The Card Display
def ascii_card(card):
    rank, _ = card
    return [
        '┌─────┐',
        f'│{rank:<5}│',
        '│  ♠  │',
        f'│{rank:>5}│',
        '└─────┘'
    ]


def ascii_hidden():
    return [
        '┌─────┐',
        '│░░░░░│',
        '│░░░░░│',
        '│░░░░░│',
        '└─────┘'
    ]


def display_hands(player_hand, dealer_hand, reveal=False):
    print("\nPlayer Hand:")
    _print_cards(player_hand)
    print(f"Total: {calculate_hand_value(player_hand)}")

    print("\nDealer Hand:")
    if reveal:
        _print_cards(dealer_hand)
        print(f"Total: {calculate_hand_value(dealer_hand)}")
    else:
        cards = [ascii_card(dealer_hand[0])] + [ascii_hidden()]
        _print_card_rows(cards)


def _print_cards(hand):
    cards = [ascii_card(c) for c in hand]
    _print_card_rows(cards)


def _print_card_rows(cards):
    for row in range(5):
        print('  '.join(card[row] for card in cards))


# Turns
def player_turn(deck, player_hand, difficulty, hand_count):
    while True:
        total = calculate_hand_value(player_hand)
        if total > 21:
            break
        choice = input("Hit or Stand? (h/s): ").lower()
        if choice == 'h':
            # Rigged logic
            if difficulty == 2 and hand_count % 5 == 0 and total >= 15:
                # force a high card (10-value if possible)
                for i in range(len(deck)):
                    if deck[i][1] == 10:
                        player_hand.append(deck.pop(i))
                        break
                else:
                    player_hand.append(draw_card(deck))
            else:
                player_hand.append(draw_card(deck))
            display_hands(player_hand, [], reveal=True)
        elif choice == 's':
            break
    return player_hand


def dealer_turn(deck, dealer_hand):
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(draw_card(deck))
    return dealer_hand


# Round Resolution

def compare_hands(player_hand, dealer_hand):
    player_total = calculate_hand_value(player_hand)
    dealer_total = calculate_hand_value(dealer_hand)

    if player_total > 21:
        return "Player busts. Dealer wins."
    if dealer_total > 21:
        return "Dealer busts. Player wins!"
    if player_total > dealer_total:
        return "Player wins!"
    if dealer_total > player_total:
        return "Dealer wins."
    return "It's a tie."


# Game Flow

def play_round(difficulty, hand_count):
    deck = create_deck()
    shuffle_deck(deck)
    player_hand, dealer_hand = initial_deal(deck)

    display_hands(player_hand, dealer_hand, reveal=False)

    if is_blackjack(player_hand):
        return "Blackjack! Player wins!"

    player_hand = player_turn(deck, player_hand, difficulty, hand_count)
    dealer_hand = dealer_turn(deck, dealer_hand)

    display_hands(player_hand, dealer_hand, reveal=True)
    return compare_hands(player_hand, dealer_hand)


def main():
    print("Welcome to Blackjack!\n")
    difficulty = int(input("Choose difficulty (1 = Normal, 2 = Fixed): "))
    hand_count = 0

    while True:
        hand_count += 1
        result = play_round(difficulty, hand_count)
        print("\nResult:", result)
        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            break

    print("Thanks for playing!")


# Run the game FINALLY 
main()
