from random import shuffle


class Deck:
    """
    Holds and manages the deck throughout the game of SkyJo
    Contains 10 of each number from -2...12
    """

    def __init__(self):
        self.deck = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] * 10
        self.shuffle_deck()

    def shuffle_deck(self):
        shuffle(self.deck)

    def draw_card(self):
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
