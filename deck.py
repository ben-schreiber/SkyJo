from random import shuffle
from card import Card


class Deck:
    """
    Holds and manages the deck throughout the game of SkyJo.
    This includes the draw pile and the put pile
    Contains 10 of each number from -2...12
    """

    def __init__(self):
        self.__draw_deck: list = [
            Card(value) for value in range(-2, 13) for _ in range(10)
        ]
        self.shuffle_deck()
        self.__put_pile = [self.draw_card()]

    def throw_card_into_put_pile(self, card: Card):
        """Throws the given card into the put pile"""
        self.__put_pile.append(card)

    def shuffle_deck(self):
        """
        Shuffles the draw deck
        """
        shuffle(self.__draw_deck)

    def draw_card(self) -> Card:
        """
        Returns the next card at the top of the draw pile.
        """
        if (
            len(self.__draw_deck) == 0
        ):  # The deck is empty, empty the put pile, shuffle it and add it to the draw pile
            self.__recycle_put_pile()
        return self.__draw_deck.pop()

    def __recycle_put_pile(self):
        """
        Takes the cards in the put pile (other than the top one), shuffles them,
        and adds them into the bottome of the draw pile
        """
        self.__draw_deck = self.__put_pile[:-1] + self.__draw_deck
        self.__put_pile = self.__put_pile[-1]
        self.shuffle_deck()

    def pop_top_of_put_pile(self) -> Card:
        """Will return the Card object at the top of the put pile. Returns None if the pile is empty"""
        if len(self.__put_pile) == 0:
            return None
        return self.__put_pile.pop()

    def peek_top_of_put_pile(self) -> Card:
        """Returns, but does not remove, the top card of the put pile. None if pile is empty"""
        if len(self.__put_pile) == 0:
            return None
        return self.__put_pile[-1]