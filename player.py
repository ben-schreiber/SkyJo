import abc
from pile import DrawPile
from card import Card
from board import Board
from typing import Tuple
import numpy as np


class Player(abc.ABC):
    def __init__(self, _id: int):
        self.id = _id
        self.board = None
        self.score = 0

    def __eq__(self, other):
        return self.id == other.id

    def went_out(self) -> bool:
        """Returns True if the player has flipped all cards in his board"""
        return not any(card.is_hidden for card in self.board)

    def init_board(self, draw_pile: DrawPile):
        """
        Initializes the player's board with the given deck
        Args:
            deck: The deck (of type Deck) to draw from
        """
        self.board = Board.from_pile(draw_pile)

    @abc.abstractmethod
    def play_turn(self, deck, last_turn: bool = False):
        raise NotImplementedError()

    def update_score(self) -> int:
        """Updates the user's overall score and returns the score for the round"""
        score = self.board.score
        self.score += score
        return score


class HumanPlayer(Player):
    """A Human player"""

    DRAW_CARD = "d"
    GRAB_TOP_OF_PILE = "g"
    SWAP_CARD = "s"
    FLIP_CARD = "f"
    VALID_USER_INPUTS_GD = {DRAW_CARD, GRAB_TOP_OF_PILE}
    VALID_USER_INPUTS_SF = {SWAP_CARD, FLIP_CARD}

    def __init__(self, _id: int):
        super().__init__(_id)

    def choose_card_on_board(self, include_flipped: bool = False) -> Tuple[int, int]:
        """Prompts the user to choose a covered card on their board"""
        row_col: str = ""
        while not row_col:
            row_col = input(
                "Please enter the row and column of the card you wish to"
                " choose:\n(Usage: <row> <col>)\n"
            )
            row_col = row_col.split()
            if len(row_col) != 2:
                row_col = ""
                print("Error! Try again!")
                continue
            try:
                row = int(row_col[0]) - 1
                col = int(row_col[1]) - 1
            except:
                row_col = ""
                print("Error! Please enter integers!")
                continue
            if not include_flipped and self.board.check_uncovered(row, col):
                row_col = ""
                print("Error! Please choose a card that is not flipped over!")
                continue
        return row, col

    def swap_card_on_board(self, card_in_hand: Card):
        """Allows the user to swap the card in his hand for one of the cards on the board"""
        row, col = self.choose_card_on_board(include_flipped=True)
        swapped_card = self.board.apply_move(row, col, card_in_hand)
        print(
            f"You swapped out a {swapped_card.get_value()} from your board for a"
            f" {card_in_hand.get_value()}"
        )
        self.deck.throw_card_into_put_pile(swapped_card)

    def flip_card(self, deck: DrawPile, card_in_hand: Card):
        """Allows the user to flip a card on the board"""
        deck.throw_card_into_put_pile(card_in_hand)
        row, col = self.__user_choose_card_on_board()
        flipped_card = self.board.apply_move(row, col)
        print(f"You flipped over a {flipped_card.get_value()}")

    def play_turn(self, deck: Deck, last_turn: bool = False):
        """
        Manages one turn of a user
        The options for a user are:
            (G) Grab the card from the put pile
            (D) Draw a card

            If the user choose (D), then there are two subsequent options as to what they can do:
            (S) Swap a card in their board with the drawn card
            (F) Throw the drawn card in the put pile and flip an a card in their board
        """
        print(f"Player {self.id}'s board is:\n{self.board}")
        g_or_d = None
        while not g_or_d:
            g_or_d = input(
                "The card on the top of the pile is"
                f" {deck.peek_top_of_put_pile().get_value()}.\nWould you like"
                " to:\n\t(G) grab the card on the top of the pile\n\t(D) draw a"
                " card?\n"
            )
            if g_or_d not in HumanPlayer.VALID_USER_INPUTS_GD:
                g_or_d = None

        if g_or_d == HumanPlayer.DRAW_CARD:
            card_in_hand: Card = deck.draw_card()
            print(f"You drew a {card_in_hand.get_value()}")
            s_or_f = None
            while not s_or_f:
                s_or_f = input(
                    f"Would you like to:\n\t(S) Swap the {card_in_hand.get_value()}"
                    " with a card in your board\n\t(F) Throw out the"
                    f" {card_in_hand.get_value()} and flip a card on your board\n"
                )
                if s_or_f not in HumanPlayer.VALID_USER_INPUTS_SF:
                    s_or_f = None

            if s_or_f == HumanPlayer.SWAP_CARD:
                self.swap_card_on_board(card_in_hand)
            elif s_or_f == HumanPlayer.FLIP_CARD:
                self.flip_card()

        elif g_or_d == HumanPlayer.GRAB_TOP_OF_PILE:
            card_in_hand: Card = deck.pop_top_of_put_pile()
            print(
                f'You now have a {card_in_hand.get_value()} in your hand; which card'
                ' would you like to swap it for?\n'
            )
            self.swap_card_on_board(card_in_hand)
