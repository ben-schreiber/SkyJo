from random import shuffle
from card import Card


class Deck:
    """
    Holds and manages the deck throughout the game of SkyJo
    Contains 10 of each number from -2...12
    """

    def __init__(self):
        self.deck: list = [Card(value) for value in range(-2, 13) for _ in range(10)]
        self.shuffle_deck()

    def shuffle_deck(self):
        shuffle(self.deck)

    def draw_card(self) -> Card:
        return self.deck.pop()

    def add_in_garbage_pile(self, pile):
        """
        Receives in the list representing the garbage pile and adds them back into the drawing pile.
        Args:
            pile: A list with the garbage pile. Not necessarily mixed
        """
        shuffle(pile)
        pile += self.deck  # Add the garbage pile to the bottom of the drawing pile
        self.deck = pile
