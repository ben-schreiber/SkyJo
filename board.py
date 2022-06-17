from __future__ import annotations

import numpy as np
from typing import Iterable

from pile import DrawPile
from card import Card


class Board:
    """
    Represents a single player's board
    """

    def __init__(self, cards: Iterable[Card]):
        if len(cards) != 12:
            raise ValueError('Must initialize board with exactly 12 cards')
        self.__board = np.array(cards, dtype=Card).reshape(3, 4)
    
    def __iter__(self):
        yield from self.__board.ravel()

    @classmethod
    def from_pile(cls, pile: DrawPile) -> Board:
        cards = [pile.draw_card() for _ in range(12)]
        for card in cards:
            card.is_hidden = True
        return cls(cards)

    def is_uncovered(self, row: int, col: int) -> bool:
        """Returns True iff the card at (row, col) is uncovered"""
        return not self.__board[row, col].is_hidden

    @property
    def score(self) -> int:
        """Returns the score of the board"""
        return sum(card for card in self if not card.is_hidden)

    @property
    def num_rows(self) -> int:
        return self.__board.shape[0]

    @property
    def num_cols(self) -> int:
        return self.__board.shape[1]

    def __str__(self) -> str:
        out_str = ""
        for row in range(self.num_rows):
            out_str += "-" * self.num_cols * 5
            out_str += "-\n"
            for col in range(self.num_cols):
                row_str = "| {:>2} "
                if self.__board[row, col].is_hidden:
                    out_str += row_str.format("X")
                else:
                    out_str += row_str.format(str(self.__board[row, col]))
            out_str += "|\n"
        out_str += "-" * self.num_cols * 5
        out_str += "-\n"
        return out_str

    def apply_move(self, row: int, col: int, card: Card = None) -> Card:
        """
        Applies the value given to the board at the position (row, col).
        If card == None, then will flip the card at the given location
        Args:
            row:
            col:
            card:
        Returns:
            The card that used to be in (row, col). Will return the card itself if card == None
        """
        if row < 0 or row >= self.num_rows:
            raise ValueError(
                f"The row entered ({row}) is outside the player's board of size"
                f" ({self.num_rows} X {self.num_cols})"
            )
        elif col < 0 or col >= self.num_cols:
            raise ValueError(
                f"The column entered ({col}) is outside the player's board of size"
                f" ({self.num_rows} X {self.num_cols})"
            )
        if card:
            to_return = self.__board[row, col]
            self.__board[row, col] = card
        else:
            self.__board[row, col].is_hidden = False
            to_return = self.__board[row, col]
        self.contract_board()
        return to_return

    def contract_board(self):
        """
        Checks the board for any row/column that is filled with one number, removes, and updates the board accordingly
        """
        check_rows = True
        check_cols = True
        while check_rows or check_cols:

            check_rows = False
            for row in range(self.num_rows):
                if (self.__board[row] == self.__board[row][0]).all():
                    self.__board = np.delete(self.__board, row, 0)
                    check_rows = True
                    break

            check_cols = False
            for col in range(self.num_cols):
                if (self.__board[:, col] == self.__board[:, col][0]).all():
                    self.__board = np.delete(self.__board, col, 1)
                    check_cols = True
                    break


if __name__ == "__main__":
    pile = DrawPile()
    board = Board.from_pile(pile)
    print(board)
    print(board.score)

    board.apply_move(0, 0)
    print(board)
    print(board.score)

    board.apply_move(0, 1)
    print(board)
    print(board.score)

    board.apply_move(0, 2)
    print(board)
    print(board.score)

    board.apply_move(0, 3)
    print(board)
    print(board.score)

    for i in range(3):
        card = Card(10)
        card.is_hidden = False
        board.apply_move(i, 2, card)
        print(board)
        print(board.score)
