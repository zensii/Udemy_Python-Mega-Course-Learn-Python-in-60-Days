import random


class Card:

    values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
              'Nine': 9, 'Ten': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

    def __init__(self, suite, rank):
        self.suite = suite
        self.rank = rank
        self.value = self.values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suite}"


class Deck:
    suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
    ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

    def __init__(self):

        self.cards = []

        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        return f'The deck has {len(self.cards)} cards in it.'


class Player:

    def __init__(self, name):

        self.player_deck = []
        self.name = name

    def play_one_card(self):
        if len(self.player_deck) > 0:
            return self.player_deck.pop(0)

    def get_cards(self, cards):

        if type(cards) is list:
            self.player_deck.extend(cards)
        else:
            self.player_deck.append(cards)

    def __str__(self):
        return f'Player {self.name} has {len(self.player_deck)} cards in his deck.'


def check_winner(first_player_card, second_player_card, at_war):

    if first_player_card.value > second_player_card.value:
        at_war = False
        return player_one, at_war
    elif first_player_card.value < second_player_card.value:
        at_war = False
        return player_two, at_war
    else:
        print('WAR!')
        at_war = True
        return None, at_war


# Create new deck and shuffle it
brand_new_deck = Deck()
brand_new_deck.shuffle()

# Initialize players
player_one = Player('Svetlin')
player_two = Player('Andi')

# Initialise players decks
for _ in range(26):
    player_one.get_cards(brand_new_deck.cards.pop(0))
    player_two.get_cards(brand_new_deck.cards.pop(0))


game_on = True
war = False
winner = None
round = 0

while game_on and round < 10000:
    round += 1
    pile = []

    first_player_play = player_one.play_one_card()
    pile.append(first_player_play)
    second_player_play = player_two.play_one_card()
    pile.append(second_player_play)
    print(f"{player_one.name} plays {first_player_play}")
    print(f"{player_two.name} plays {second_player_play}")

    winner, war = check_winner(first_player_play, second_player_play, war)

    while war:
        if len(player_one.player_deck) < 4:
            print(f"{player_one.name} does not have enough cards to participate in the war!")
            winner = player_two
            game_on = False
            break
        elif len(player_two.player_deck) < 4:
            print(f"{player_two.name} does not have enough cards to participate in the war!")
            winner = player_one
            game_on = False
            break
        else:
            print('Each player stakes 3 cards: ')
            player_one_stake = None
            player_two_stake = None
            for stake in range(4):
                player_one_stake = player_one.play_one_card()
                print(f"{player_one.name} stakes {player_one_stake}")
                pile.append(player_one_stake)
                player_two_stake = player_two.play_one_card()
                print(f"{player_two.name} stakes {player_two_stake}")
                pile.append(player_two_stake)

            winner, war = check_winner(player_one_stake, player_two_stake, war)

    winner.get_cards(pile)

    if len(player_one.player_deck) == 0:
        winner = player_two
        game_on = False
        break
    elif len(player_two.player_deck) == 0:
        winner = player_one
        game_on = False
        break

    if game_on:
        print(f"{winner.name} wins the round!")
        print()
        print('Starting next round.')
        print(player_one)
        print(player_two)
        random.shuffle(player_one.player_deck)
        random.shuffle(player_two.player_deck)
print(f"{winner.name} wins the game!")
print(round)