import random


class Card:

    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
              '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

    def __init__(self, suite, rank):
        self.suite = suite
        self.rank = rank
        self.value = self.values[rank]

    def __str__(self):

        return self.rank + ' of ' + self.suite


class Deck:
    suits = (chr(9827), chr(9830), chr(9829), chr(9824))
    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

    def __init__(self):
        self.cards = []
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def add_cards(self, cards):
        self.cards.extend(cards)

    def deal_one(self):
        return self.cards.pop(0)


class Player:

    def __init__(self, name, bank):
        self.player_hand = []
        self.name = name
        self.bank = bank

    def hit(self, card):
        self.player_hand.append(card)

    def bid(self, amount):
        if amount <= self.bank:
            self.bank -= amount
            print(f"{self.name} bids {amount}")
            return True
        else:
            print("You do not have enough money!")
            return False

    def current_hand_value(self):
        totals = []
        total = sum(card.value for card in self.player_hand)
        totals.append(total)
        # count how many aces the player has in his hand
        aces = ['A' in str(card) for card in self.player_hand].count(True)
        for _ in range(aces):
            value = total - 10
            totals.append(value)
        return totals

    def display_cards(self):
        """Display all the cards in the cards list."""
        rows = ['', '', '', '', '']  # The text to display on each row.

        for i, card in enumerate(self.player_hand):
            rank, suit = card.rank, card.suite
            rows[0] += ' ___  '
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))
        for row in rows:
            print(row)

    def __str__(self):
        return f'Player {self.name} has {self.bank}$ in his account.'


class Dealer(Player):

    def __init__(self):
        Player.__init__(self, name=None, bank=None)


def get_bid():

    while True:
        bid = 0
        try:
            bid = int(input(f"How much would you like to bid: "))
            if bid <= player_one.bank:
                print("Bid accepted!")
                player_one.bid(bid)
                break
            else:
                print('You do not have enough money!')
        except ValueError:
            print("please enter a valid number!")

    return bid


def deal_cards():
    print()
    print('Dealing cards...')
    # Deal 2 cards for player
    player_one.hit(game_deck.deal_one())
    player_one.hit(game_deck.deal_one())
    print(f"{player_one.name}'s current hand value: {player_one.current_hand_value()}")
    player_one.display_cards()

    # Deal 1 cards for dealer
    dealer.hit(game_deck.deal_one())
    print(f"Dealer's current hand value: {dealer.current_hand_value()}")
    dealer.display_cards()
    print()


# Initiate deck and player
game_deck = Deck()
player_one = Player('Svetlin', 1000)
dealer = Dealer()

# START GAME

game_on = True

while game_on:

    winner = None
    print(player_one)
    if player_one.bank == 0:
        print('Sorry you are bankrupt.Go get a fast loan and come back!')
        break

    # Bidding
    bid = get_bid()

    # deal initial cards
    random.shuffle(game_deck.cards)
    deal_cards()

    while True:
        print()
        choice = input("What would you like to do? Hit or Pass: ")

        if 21 in player_one.current_hand_value():
            print(f"BlackJack! {player_one.name} wins the round.")
            winner = player_one
            break
        match choice:
            case 'Hit':
                player_one.hit(game_deck.deal_one())
                player_one.display_cards()
                print(f"{player_one.name}'s current hand value: {player_one.current_hand_value()}")

            case 'Pass':
                break  # dealer should start

        if player_one.current_hand_value()[-1] > 21:
            print(f"{player_one.name} is BUST! The house wins.")
            winner = dealer
            break

        print(f"Dealer's current hand value: {dealer.current_hand_value()}")

    # dealer turn
    while winner != dealer and winner != player_one and dealer.current_hand_value()[-1] < 21:
        print()
        print('Dealer draws a card.')
        dealer.hit(game_deck.deal_one())
        dealer.display_cards()
        print(f"Dealer's current hand value: {str(dealer.current_hand_value())}")

        if dealer.current_hand_value()[-1] > 21:
            print("Dealer is BUST!")
            print(f"{player_one.name} wins the round!")
            winner = player_one
            break
        if 21 in dealer.current_hand_value():
            print(f"BlackJack! Dealer wins the round.")
            winner = dealer
        if max(filter(lambda x: x < 21, dealer.current_hand_value())) > max(filter(lambda x: x < 21, player_one.current_hand_value())):
            print('The dealer wins the round!')
            winner = dealer

    # collecting pot if won
    if winner == player_one:
        player_one.bank += bid * 2
        print(f"{player_one.name} wins {bid*2}$")
        print(player_one)

    # Play again question
    print()
    play_again = input("Would you like to play another round? Yes or No: ")
    if play_again == 'No':
        print("Thanks for playing! Bye.")
        game_on = False
    else:
        game_deck.add_cards(player_one.player_hand)
        game_deck.add_cards(dealer.player_hand)
        player_one.player_hand.clear()
        dealer.player_hand.clear()
        print(40 * '\n')

print("Exiting....")
