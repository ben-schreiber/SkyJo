from __future__ import annotations

from typing import Union


class Card:
    def __init__(self, number: int):
        if number < -2 or number > 12:
            raise ValueError(f"The value {number} provided is not legal. Must be in the range [-2, 12]")
        self.number = number
        self.is_hidden = True
    
    def __eq__(self, other: Card) -> bool:
        return self.number == other.number
    
    def __str__(self) -> str:
        return str(self.number)
    
    def __repr__(self) -> str:
        return f'Card({self.number=}, {self.is_hidden=})'

    def __add__(self, other: Union[int, Card]) -> int:
        """
        Returns the sum of the values of the two cards
        """
        if isinstance(other, int):
            return self.number + other
        return self.number + other.number

    def __radd__(self, other: Union[int, Card]) -> int:
        """
        Returns the sum of the values of the two cards
        """
        if isinstance(other, int):
            return self.number + other
        return self.number + other.number

    def __lt__(self, other: Card) -> bool:
        return self.number < other.number
