import numpy as np
from deck import Deck
from card import Card


class Board:
    """
    Represents a single player's board
    """

    def __init__(self, deck: Deck):
        self.board = np.array(
            [deck.draw_card() for _ in range(12)], dtype=Card
        ).reshape(3, 4)
        self.board[0, 0].flip_over()
        self.board[0, 1].flip_over()

    def check_uncovered(self, row: int, col: int) -> bool:
        """Returns True iff the card at (row, col) is uncovered"""
        return not self.board[row, col].is_hidden()

    def get_score(self) -> int:
        """Returns the score of the board"""
        return np.sum(np.vectorize(Card.get_value)(self.board.ravel()))

    @property
    def num_rows(self) -> int:
        return self.board.shape[0]

    @property
    def num_cols(self) -> int:
        return self.board.shape[1]

    def __str__(self) -> str:
        out_str = ""
        for row in range(self.num_rows):
            out_str += "-" * self.num_cols * 5
            out_str += "-\n"
            for col in range(self.num_cols):
                row_str = "| {:>2} "
                if self.board[row, col].is_hidden():
                    out_str += row_str.format("X")
                else:
                    out_str += row_str.format(self.board[row, col].get_value())
            out_str += "|\n"
        out_str += "-" * self.num_cols * 5
        out_str += "-\n"
        return out_str

    def get_board(self):
        return self.board

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
        else:
            if card:
                to_return = self.board[row, col]
                self.board[row, col] = card
            else:
                self.board[row, col].flip_over()
                to_return = self.board[row, col]
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
                bool_arr = self.board[row] == self.board[row][0]
                if np.all(bool_arr):
                    self.board = np.delete(self.board, row, 0)
                    check_rows = True
                    break

            check_cols = False
            for col in range(self.num_cols):
                bool_arr = self.board[:, col] == self.board[:, col][0]
                if np.all(bool_arr):
                    self.board = np.delete(self.board, col, 1)
                    check_cols = True
                    break


if __name__ == "__main__":
    deck = Deck()
    board = Board(deck)
    print(board)
    board.apply_move(0, 0, Card(12))
    print(board)
    board.apply_move(0, 1, Card(12))
    print(board)
    board.apply_move(0, 2, Card(12))
    print(board)
    board.apply_move(0, 3, Card(12))
    print(board)
