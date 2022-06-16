from __future__ import annotations

import abc
from random import shuffle
from typing import List, Union, Optional, Iterable

from card import Card
from errors import EmptyPileError


class Pile(abc.ABC):

    def __init__(self, other_pile: Optional[Pile] = None):
        if other_pile:
            self._pile = list(other_pile._pile)
        else:
            self._pile = self._init_fresh_pile()

    @abc.abstractmethod
    def _init_fresh_pile(self) -> List[Card]:
        raise NotImplementedError()

    def __bool__(self) -> bool:
        """
        Returns `True` if the pile is not empty
        """
        return len(self._pile) != 0

    def is_empty(self) -> bool:
        return not bool(self)
    
    def __len__(self) -> int:
        return len(self._pile)

    def __getitem__(self, item: int) -> Card:
        return self._pile[item]

    
class PutPile(Pile):

    def _init_fresh_pile(self) -> List[Card]:
        return []

    def __add__(self, other: Union[Card, Iterable[Card]]) -> Pile:
        for card in (new_pile := list(other)):
            card.is_hidden = False
        return Pile(self._pile + new_pile)
    
    def __iadd__(self, other: Union[Card, Iterable[Card]]):
        for card in (new_pile := list(other)):
            card.is_hidden = False
        self._pile += new_pile


class DrawPile(Pile):
    """
    Holds and manages the deck throughout the game of SkyJo.
    This includes the draw pile and the put pile
    Contains 10 of each number from -2...12
    """

    def _init_fresh_pile(self):
        deck = (
            [
                Card(value)
                for value in (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                for _ in range(10)
            ]
            + [Card(-2) for _ in range(5)]
            + [Card(0) for _ in range(15)]
        )
        shuffle(deck)
        return deck

    def __iter__(self):
        while True:
            yield self.draw_card()

    def __add__(self, other: Union[Pile, Iterable[Card]]) -> Pile:
        new_pile = other._pile if isinstance(other, Pile) else list(other)
        shuffle(new_pile)
        new_pile += self._pile
        for card in new_pile:
            card.is_hidden = True
        return Pile(new_pile)
    
    def __iadd__(self, other: Union[Card, Pile, Iterable[Card]]):
        new_pile = other._pile if isinstance(other, Pile) else list(other)
        shuffle(new_pile)
        self._pile = new_pile + self._pile
        for card in self._pile:
            card.is_hidden = True

    def draw_card(self) -> Card:
        """
        Returns the next card at the top of the draw pile.
        """
        if not self:
            raise EmptyPileError()
        card = self._pile.pop()
        card.is_hidden = False
        return card
