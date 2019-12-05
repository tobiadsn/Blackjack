import random

suits = ('Hearts','Diamond','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

playing = True

class Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank+  'of'  +self.suit

class Deck:
    def __init__(self):
        self.deck = [] # empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' +card.__str__()
        return "The deck has : " +deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

# test_deck = Deck()
# test_deck.shuffle()
# print(test_deck)

class Hand:  # Represent what cards are currently in someone's hand
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # add an attribute to keep track of your aces

    def add_card(self,card):
        # card passed in from Deck.deal() --> single card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]


# test_deck = Deck()
# test_deck.shuffle()
# Player
# test_player = Hand()
# Deal 1 card from DeckCard=(suit,rank)
# pulled_card = test_deck.deal()
# print(pulled_card)
# test_player.add_card(pulled_card)
# print(test_player.value)

        # Track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        # If total value > 21 and I still have an ace
        # Then change my ace to be a 1 instead of an 11

        while self.value > 21 and self.aces: # or self.aces > 0
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self,total = 100): # The total will reset automatically when you play again. You can make it recurring by assigning it to a certain player
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:

        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("Sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print(f'Sorry, you do not have enough chips! You only have: {chips.total}')
            else:
                break


def hit(deck,hand):

    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):

    global playing # to control an upcoming while loop

    while True:
        x = input('Do you want to hit or stand? Enter h or s ')

        if x.lower() == 'h':
            hit(deck,hand)
        elif x.lower() == 's':
            print("Player Stands Dealer's Turn")
            playing = False

        else:
            print("Sorry, I did not understand that, Please enter h or s only!!")
            continue

        break


def show_some(player,dealer):
    print("\nDealer's Hand: ")
    print(" <card hidden>")
    print('',dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ') # * is used to print every item in a collection and the sep='\n' arguments print each item on a separate line

def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep = '\n')
    print("Player's Hand =",player.value)


def player_busts(player,dealer,chips):
    print("PLAYER BUSTED")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("PLAYER WINS")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("DEALER BUSTED! PLAYER WINS")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("DEALER WINS")
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and Player tie! PUSH")



# GAMEPLAY

while True:

    print("WELCOME TO BLACKJACK")
    # Create & shuffle the deck, then deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())


    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the player for their bet
    take_bet(player_chips)

    # Show cards(but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    while playing:
        # Prompt for player to hit or stand
        hit_or_stand(deck,player_hand)

        # Show some cards(but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)

        # If player's hand exceeds 21, run player_busts(), and break out of the loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)

            break

    # If player's hand hasn't busted, play Dealer's hand until it reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        # Show all cards
        show_all(player_hand,dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)


    # Inform Player of their total chips
    print(f'\n Player total chips are at : {player_chips.total}')
    # Ask to play again
    new_game = input("Would you like to play again? y/n")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break














