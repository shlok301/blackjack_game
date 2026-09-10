import random
import art

print(art.logo)

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["♠", "♥", "♦", "♣"]
VALUES = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}

MIN_BET = 10
MAX_BET = 100


def build_deck():
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck


def draw_card(deck):
    if not deck:
        deck.extend(build_deck())
    return deck.pop()


def card_str(card):
    rank, suit = card
    return f"{rank}{suit}"


def hand_to_list(hand):
    return [card_str(card) for card in hand]


def card_sum(hand):
    total = sum(VALUES[rank] for rank, _ in hand)
    aces = sum(1 for rank, _ in hand if rank == "A")
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total


def is_blackjack(hand):
    return len(hand) == 2 and card_sum(hand) == 21


def can_split(hand):
    return len(hand) == 2 and VALUES[hand[0][0]] == VALUES[hand[1][0]]


def ask_choice(prompt, valid):
    while True:
        answer = input(prompt).strip().lower()
        if answer in valid:
            return answer
        print(f"Please enter one of: {', '.join(valid)}")


def ask_bid(balance):
    while True:
        raw = input(
            f"How much ₹ would you like to bid? (Min {MIN_BET} and Max {MAX_BET}): "
        ).strip()
        try:
            amount = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if amount < MIN_BET or amount > MAX_BET:
            print(f"Please enter a value between {MIN_BET} and {MAX_BET}.")
            continue
        if amount > balance:
            print("You don't have enough balance for that bid.")
            continue
        return amount


def show_dealer(dealer_hand, reveal=False):
    if reveal:
        print(f"Dealer: {hand_to_list(dealer_hand)}, Score: {card_sum(dealer_hand)}")
    else:
        print(f"Dealer: [{card_str(dealer_hand[0])}, ??]")


def show_hand(label, hand):
    print(f"{label}: {hand_to_list(hand)}, Score: {card_sum(hand)}")


def play_out_hand(deck, hand, is_split_ace=False):
    if is_split_ace:
        hand.append(draw_card(deck))
        show_hand("Hand", hand)
        return
    while card_sum(hand) < 21:
        action = ask_choice(
            f"Hand {hand_to_list(hand)} (Score: {card_sum(hand)}) — 'h' to hit, 's' to stand: ",
            ["h", "s"],
        )
        if action == "h":
            hand.append(draw_card(deck))
            print(f"You drew {card_str(hand[-1])}.")
            show_hand("Hand", hand)
            if card_sum(hand) > 21:
                print("Bust! This hand is over.")
        else:
            return


def dealer_play(deck, dealer_hand):
    while card_sum(dealer_hand) < 17:
        dealer_hand.append(draw_card(deck))


def settle_hand(hand, dealer_hand, bet, blackjack_eligible):
    total = card_sum(hand)
    dealer_total = card_sum(dealer_hand)

    if total > 21:
        return "computer", 0

    dealer_bj = is_blackjack(dealer_hand)

    if blackjack_eligible and is_blackjack(hand) and not dealer_bj:
        return "user_blackjack", bet + int(bet * 1.5)
    if blackjack_eligible and is_blackjack(hand) and dealer_bj:
        return "draw", bet
    if dealer_total > 21:
        return "user", bet * 2
    if total > dealer_total:
        return "user", bet * 2
    if total < dealer_total:
        return "computer", 0
    return "draw", bet


def announce(result, bet, payout, prefix=""):
    if result == "user_blackjack":
        print(f"{prefix}Blackjack! You win ₹{payout - bet}.")
    elif result == "user":
        print(f"{prefix}You win ₹{payout - bet}.")
    elif result == "draw":
        print(f"{prefix}Push — your ₹{bet} bet is returned.")
    else:
        print(f"{prefix}You lose ₹{bet}.")


def play_round(deck, balance, bid_amount, bidding):
    player_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]

    show_dealer(dealer_hand)
    show_hand("Your hand", player_hand)

    if is_blackjack(player_hand) or is_blackjack(dealer_hand):
        show_dealer(dealer_hand, reveal=True)
        result, payout = settle_hand(player_hand, dealer_hand, bid_amount, True)
        if bidding:
            balance += payout
        announce(result, bid_amount, payout)
        return balance

    hands = [player_hand]
    bets = [bid_amount]

    if can_split(player_hand) and (not bidding or balance >= bid_amount):
        split_choice = ask_choice(
            "Your first two cards match — split? (y/n): ", ["y", "n"]
        )
        if split_choice == "y":
            if bidding:
                balance -= bid_amount
                print(
                    f"You've decided to split, so an additional ₹{bid_amount} is deducted.\nCurrent balance ₹{balance}"
                )
            is_ace_split = player_hand[0][0] == "A"
            hand_1 = [player_hand[0], draw_card(deck)]
            hand_2 = [player_hand[1], draw_card(deck)]
            hands = [hand_1, hand_2]
            bets = [bid_amount, bid_amount]
            print(
                f"Split into two hands: {hand_to_list(hand_1)} and {hand_to_list(hand_2)}"
            )
            for hand in hands:
                play_out_hand(deck, hand, is_split_ace=is_ace_split)
        else:
            play_out_hand(deck, player_hand)
    else:
        play_out_hand(deck, player_hand)

    if any(card_sum(hand) <= 21 for hand in hands):
        dealer_play(deck, dealer_hand)

    show_dealer(dealer_hand, reveal=True)

    for index, (hand, bet) in enumerate(zip(hands, bets), start=1):
        prefix = f"Hand {index}: " if len(hands) > 1 else ""
        show_hand(f"Hand {index}" if len(hands) > 1 else "Your final hand", hand)
        result, payout = settle_hand(hand, dealer_hand, bet, len(hands) == 1)
        if bidding:
            balance += payout
        announce(result, bet, payout, prefix=prefix)

    return balance


def game_start(deck, name, balance, returning, force_no_bid=False):
    greeting = (
        f"Hello {name}, welcome back to Blackjack."
        if returning
        else f"Hello {name}, welcome to Blackjack."
    )
    print(greeting)

    if force_no_bid:
        want_bid = "no bid"
    else:
        want_bid = ask_choice(
            "Type 'bid' to bid, or 'no bid' to play friendly: ", ["bid", "no bid"]
        )

    if want_bid == "bid":
        print(f"Your current balance is ₹{balance}")
        bid_amount = ask_bid(balance)
        balance -= bid_amount
        print(f"You've bid ₹{bid_amount}, current balance ₹{balance}")
        balance = play_round(deck, balance, bid_amount, bidding=True)
    else:
        play_round(deck, 0, 0, bidding=False)
        print("Thanks for playing!")

    return balance


def main():
    deck = build_deck()
    end_of_game = False
    same_user = "no"
    balance = 1000
    user_name = ""

    while not end_of_game:
        if same_user == "no":
            want_to_play = ask_choice(
                "Do you want to play a game of Blackjack? Type 'y' or 'n': ", ["y", "n"]
            )
            if want_to_play == "n":
                end_of_game = True
                print("Okay. Thank you!")
                continue
            user_name = input("Please enter your name: ").strip() or "Player"
            balance = 1000
            balance = game_start(deck, user_name, balance, returning=False)
            same_user = ask_choice(
                "Would you like to continue with the same user? Type 'yes' or 'no': ",
                ["yes", "no"],
            )

        else:
            if balance < MIN_BET:
                force_no_bid = ask_choice(
                    "Would you like to continue without any bid? Type 'yes' or 'no': ",
                    ["yes", "no"],
                )
                if force_no_bid == "no":
                    print(f"Thank you {user_name} for playing blackjack.")
                    end_of_game = True
                    continue
                balance = game_start(
                    deck, user_name, 0, returning=True, force_no_bid=True
                )
            else:
                balance = game_start(deck, user_name, balance, returning=True)

            same_user = ask_choice(
                "Would you like to continue with the same user? Type 'yes' or 'no': ",
                ["yes", "no"],
            )

    print(f"\nThanks for playing, {user_name}! Final balance: ₹{balance}")


if __name__ == "__main__":
    main()
