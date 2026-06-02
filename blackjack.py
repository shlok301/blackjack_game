import random
import art

print(art.logo)


def bids(
    balance,
    bid_amount,
    result=None,
):
    if result == "draw":
        balance += bid_amount
        print(f"You bet has been pushed back.\nCurrent Balance: {balance}")
    elif result == "user":
        balance += 2 * bid_amount
        print(f"You won ₹{bid_amount}.\nCurrent Balance: {balance}")
    elif result in ("computer", "computer_blackjack"):
        print(f"You lost ₹{bid_amount}.\nCurrent Balance: {balance}")
    elif result == "user_blackjack":
        balance += 2.5 * bid_amount
        print(f"You won ₹{1.5*bid_amount}.\nCurrent Balance: {balance}")
    return balance


def card_sum(cards):
    return sum(value for _, value in cards)


def dealer(available, bid, choice):
    cards = {
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
    user_cards = [
        (card, cards[card]) for card in random.choices(list(cards.keys()), k=2)
    ]
    user_sum = card_sum(user_cards)
    print(f"Your cards: {[card for card, _ in user_cards]}, Score: {user_sum}")
    computer_cards = [
        (card, cards[card]) for card in random.choices(list(cards.keys()), k=2)
    ]
    computer_sum = card_sum(computer_cards)
    print(f"Computer's first card: {computer_cards[0][0]}")
    available = blackjack(
        user_cards, computer_cards, user_sum, computer_sum, available, bid, choice
    )
    return available


def compare(user_total, computer_total):
    if computer_total > 21:
        return "user"
    elif user_total < computer_total:
        return "computer"
    elif user_total > computer_total:
        return "user"
    else:
        return "draw"


def split_new_card(
    cards,
    user_cards,
    computer_cards,
    user_total,
    computer_total,
    last_hand="no",
    hand_1_total=None,
):
    while user_total <= 21:
        another_card = input(
            f"Type 'y' to get another card for the hand {[card for card,_ in user_cards]}, type 'n' to pass: "
        ).lower()

        if another_card == "y":
            new_card = random.choice(list(cards.keys()))
            user_cards.append((new_card, cards[new_card]))
            user_total = card_sum(user_cards)
            if user_total <= 21:
                print(
                    f"Your cards: {[card for card,_ in user_cards]}, Score: {user_total}"
                )
                print(f"Computer's first card: {computer_cards[0][0]}")
            else:
                if ("A", 11) in user_cards:
                    idx = user_cards.index(("A", 11))
                    user_cards[idx] = ("A", 1)
                    user_total = card_sum(user_cards)
                    print(
                        f"Your cards: {[card for card,_ in user_cards]}, Score: {user_total}"
                    )
                    print(f"Computer's first card: {computer_cards[0][0]}")
                    continue
                else:
                    print(
                        f"Your final hand: {[card for card,_ in user_cards]}, Score: {user_total}"
                    )
                    print(
                        f"Computer's final hand: {[card for card,_ in computer_cards]}, Score: {computer_total}"
                    )
                    print("Oops! Sorry, you went over 21. You lose 😭.")
                    if last_hand == "no":
                        return user_total
                    else:
                        result_hand_2 = "computer"
                        result_hand_1 = compare(hand_1_total, computer_total)
                        return result_hand_1, result_hand_2

        elif another_card == "n":
            if last_hand == "no":
                return user_total
            else:
                while computer_total < 17:
                    new_card = random.choice(list(cards.keys()))
                    computer_cards.append((new_card, cards[new_card]))
                    computer_total = card_sum(computer_cards)
                print(
                    f"Your final hand: {[card for card,_ in user_cards]}, Score: {user_total}"
                )
                print(
                    f"Computer's final hand: {[card for card,_ in computer_cards]}, Score: {computer_total}"
                )
                result_hand_1 = compare(hand_1_total, computer_total)
                result_hand_2 = compare(user_total, computer_total)
                return result_hand_1, result_hand_2

        else:
            print("Please select a valid choice.")


def new_cards(
    cards,
    user_cards,
    computer_cards,
    user_total,
    computer_total,
):
    result = None
    while user_total <= 21:
        another_card = input("Type 'y' to get another card, type 'n' to pass: ").lower()
        if another_card == "y":
            new_card = random.choice(list(cards.keys()))
            user_cards.append((new_card, cards[new_card]))
            user_total = card_sum(user_cards)
            if user_total <= 21:
                print(
                    f"Your cards: {[card for card,_ in user_cards]}, Score: {user_total}"
                )
                print(f"Computer's first card: {computer_cards[0][0]}")
            else:
                if ("A", 11) in user_cards:
                    idx = user_cards.index(("A", 11))
                    user_cards[idx] = ("A", 1)
                    user_total = card_sum(user_cards)
                    print(
                        f"Your cards: {[card for card,_ in user_cards]}, Score: {user_total}"
                    )
                    print(f"Computer's first card: {computer_cards[0][0]}")
                    continue
                else:
                    print(
                        f"Your final hand: {[card for card,_ in user_cards]}, Score: {user_total}"
                    )
                    print(
                        f"Computer's final hand: {[card for card,_ in computer_cards]}, Score: {computer_total}"
                    )
                    print("Oops! Sorry, you went over 21. You lose 😭.")
                    result = "computer"

        elif another_card == "n":
            while computer_total < 17:
                new_card = random.choice(list(cards.keys()))
                computer_cards.append((new_card, cards[new_card]))
                computer_total = card_sum(computer_cards)
            print(
                f"Your final hand: {[card for card,_ in user_cards]}, Score: {user_total}"
            )
            print(
                f"Computer's final hand: {[card for card,_ in computer_cards]}, Score: {computer_total}"
            )
            if computer_total > 21:
                print("Computer's hand is bust, goes over 21. You win.")
                result = "user"
            elif user_total < computer_total:
                print("Computer Wins")
                result = "computer"
            elif user_total > computer_total:
                print("You win.")
                result = "user"
            else:
                print("It's a Draw.")
                result = "draw"
            break

        else:
            print("Please select a valid choice.")
    return result


def blackjack(
    user_cards,
    computer_cards,
    user_total,
    computer_total,
    total_amount=0,
    bid_value=0,
    bid_choice=None,
):
    split = "no"
    cards = {
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

    if (user_total == 21 and len(user_cards) == 2) and (
        computer_total == 21 and len(computer_cards) == 2
    ):
        print("it's a draw.")
        result = "draw"

    elif (user_total == 21 and len(user_cards) == 2) and computer_total != 21:
        print("It's a Blackjack. You win.")
        result = "user_blackjack"

    elif (user_total == 21 and len(user_cards) != 2) and (
        computer_total == 21 and len(computer_cards) == 2
    ):
        print("It's a Blackjack for Computer. You lose.")
        result = "computer_blackjack"

    elif (user_total == 21 and len(user_cards) != 2) and (
        computer_total == 21 and len(computer_cards) != 2
    ):
        print("it's a draw.")
        result = "draw"

    elif (user_cards[0][1] == user_cards[1][1]) and len(user_cards) == 2:
        split = input("Would you like to split? Type 'yes' or 'no': ").lower()
        if split == "yes":
            user_hand_1 = [user_cards[0]]
            new_card = random.choice(list(cards.keys()))
            user_hand_1.append((new_card, cards[new_card]))
            user_total_hand_1 = card_sum(user_hand_1)
            user_hand_2 = [user_cards[1]]
            new_card = random.choice(list(cards.keys()))
            user_hand_2.append((new_card, cards[new_card]))
            user_total_hand_2 = card_sum(user_hand_2)
            if bid_choice == "bid":
                total_amount -= bid_value
                print(
                    f"You've decided to split, so an additional {bid_value} is dedcuted from you account.\nCurrent balance {total_amount}"
                )
                print(
                    f"To summarize you now have two hands one {[card for card,_ in user_hand_1]} with bid of {bid_value}, and another {[card for card,_ in user_hand_2]} with bid of {bid_value}."
                )
                user_result = split_new_card(
                    cards,
                    user_hand_1,
                    computer_cards,
                    user_total_hand_1,
                    computer_total,
                    "no",
                )
                result_1, result_2 = split_new_card(
                    cards,
                    user_hand_2,
                    computer_cards,
                    user_total_hand_2,
                    computer_total,
                    "yes",
                    user_result,
                )
            else:
                print("You've decided to split.")
                print(
                    f"To summarize you now have two hands one {[card for card,_ in user_hand_1]} with bid of {bid_value}, and another {[card for card,_ in user_hand_2]} with bid of {bid_value}."
                )

    else:
        result = new_cards(
            cards, user_cards, computer_cards, user_total, computer_total
        )

    if bid_choice == "bid" and split == "yes":
        available = bids(
            total_amount,
            bid_value,
            result_1,
        )
        available = bids(
            available,
            bid_value,
            result_2,
        )
        return available

    if bid_choice == "bid":
        available = bids(
            total_amount,
            bid_value,
            result,
        )
        return available

    else:
        print("Thanks for playing!")


def game_start(name, available_balance, user, force_user=None):
    if force_user == "yes":
        want_bid = "no bid"
    else:
        want_bid = input(
            "Type 'bid' to bid, or type 'no bid' to play friendly: "
        ).lower()
    if user == "no":
        print(f"Hello {name}, welcome to Blackjack.")
    elif user == "yes":
        print(f"Hello {name}, welcome back to Blackjack.")
    if (want_bid == "bid") and (available_balance >= 10):
        print(f"Your current balance is {available_balance}")
        bid_amount = int(
            input("How much ₹ would you like to bid?(Min 10 and Max 100.) ")
        )
        if 10 <= bid_amount <= 100:
            available_balance -= bid_amount
            print(f"You've bid ₹{bid_amount}, current balance {available_balance}")
            available_balance = dealer(available_balance, bid_amount, want_bid)
            return available_balance
        else:
            print("You've entered an invalid bid amount.")
            return available_balance
    elif want_bid == "no bid":
        dealer(0, 0, want_bid)
    else:
        print("Something is not right.")
        return available_balance


end_of_game = False
same_user = "no"
while not end_of_game:
    if same_user == "no":
        balance = 1000
        want_to_play = input(
            "Do you want to play a game of Blackjack? Type 'y' or 'n': "
        ).lower()
        if want_to_play == "y":
            user_name = input("Please enter you name: ")
            balance = game_start(user_name, balance, same_user)
            same_user = input(
                "Would you like to continue with the same user? Type 'yes' or 'no': "
            ).lower()
        elif want_to_play == "n":
            end_of_game = True
            print("Okay. Thank you!")
        else:
            print("Please enter a valid choice.")

    elif same_user == "yes":
        print(f"Hello {user_name}, please play again.")
        if balance < 10:
            force_no_bid = input(
                "Would you like to continue with out any bid? Type 'yes' or 'no': "
            ).lower()
            if force_no_bid == "yes":
                balance = game_start(user_name, 0, same_user, force_no_bid)
            elif force_no_bid == "no":
                print(f"Thank you {user_name} for playing blackjack.")
                end_of_game = True
                continue
            else:
                print(
                    "Sorry! You didn't enter the correct choice. So, you've been removed from the game."
                )
                end_of_game = True
                continue
        else:
            balance = game_start(user_name, balance, same_user)
        same_user = input(
            "Would you like to continue with the same user? Type 'yes' or 'no': "
        ).lower()

    else:
        print("Sorry! Please enter a valid choice.")
        break
