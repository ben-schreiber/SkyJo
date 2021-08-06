from random import shuffle
from card import Card
import numpy as np


class Deck:
    """
    Holds and manages the deck throughout the game of SkyJo.
    This includes the draw pile and the put pile
    Contains 10 of each number from -2...12
    """

    def __init__(self):
        self.__draw_deck: list = (
            [
                Card(value)
                for value in (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                for _ in range(10)
            ]
            + [Card(-2) for _ in range(5)]
            + [Card(0) for _ in range(15)]
        )
        self.shuffle_deck()
        self.__put_pile = [self.draw_card()]

    def throw_card_into_put_pile(self, card: Card):
        """Throws the given card into the put pile"""
        card.flip_over(facing = 'up')
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
        card = self.__draw_deck.pop()
        card.flip_over(facing = 'up')
        return card

    def __recycle_put_pile(self):
        """
        Takes the cards in the put pile (other than the top one), shuffles them,
        and adds them into the bottome of the draw pile
        """
        cards_to_recycle = self.__put_pile[:-1]
        np.vectorize(Card.flip_over)(cards_to_recycle)
        self.__draw_deck = cards_to_recycle + self.__draw_deck
        self.__put_pile = self.__put_pile[-1]
        self.shuffle_deck()

    def pop_top_of_put_pile(self) -> Card:
        """Will return the Card object at the top of the put pile. Returns None if the pile is empty"""
        if len(self.__put_pile) == 0:
            return None
        val = self.__put_pile.pop()
        return val

    def peek_top_of_put_pile(self) -> Card:
        """Returns, but does not remove, the top card of the put pile. None if pile is empty"""
        if len(self.__put_pile) == 0:
            return None
        return self.__put_pile[-1]
