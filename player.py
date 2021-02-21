from deck import Deck
from card import Card


class Player:

    USER_PLAYER: int = 0
    CPU_PLAYER: int = 1
    DRAW_CARD: str = 'd'
    GRAB_TOP_OF_PILE: str = 'g'
    SWAP_CARD: str = 's'
    FLIP_CARD: str = 'f'
    VALID_USER_INPUTS = {DRAW_CARD, GRAB_TOP_OF_PILE}

    def __init__(self, _id: int, player_type: int = Player.USER_PLAYER):
        self.id = _id
        self.board: Board = None
        self.score: int = 0
        self.player_type: str = player_type
    
    def __eq__(self, other):
        return self.id = other.id
    
    def get_id(self) -> int:
        return self.id

    def went_out(self) -> bool:
        """Returns True if the player has flipped all cards in his board"""
        return not np.any(np.vectorize(Card.is_hidden)(self.board.get_board().ravel()))

    def init_board(self, deck: Deck):
        """
        Initializes the player's board with the given deck
        Args:
            deck: The deck (of type Deck) to draw from
        """
        self.board = Board(deck)

    def get_score(self) -> int:
        """
        Returns the player's score for the course of the game
        """
        return self.score

    def __user_turn(self, deck: Deck, last_turn: bool):
        """
        Manages one turn of a user
        The options for a user are:
            (G) Grab the card from the put pile
            (D) Draw a card

            If the user choose (D), then there are two subsequent options as to what they can do:
            (S) Swap a card in their board with the drawn card
            (F) Throw the drawn card in the put pile and flip an a card in their board
        """
        g_or_d = None
        while not g_or_d:
            g_or_d = input(f'The card on the top of the pile is {deck.peek_top_of_put_pile()}.\n \
                            Last turn? {last_turn}\n\
                            Would you like to:\n\
                                \t(G) grab the card on the top of the pile\n\
                                \t(D) draw a card?')
            if g_or_d not in Player.VALID_USER_INPUTS:
                g_or_d = None

        if g_or_d == Player.DRAW_CARD:
            card_in_hand: Card = deck.draw_card()
            print(f'You drew a {card_in_hand.get_value()}')
            s_or_f = None
            while not s_or_f:
                s_or_f = input(f'Would you like to:\n\
                                    \t(S) Swap the {card_in_hand.get_value()} with a card in your board\n\
                                    \t(F) Throw out the {card_in_hand.get_value()} and flip a card on your board')
                
        else:
            card_in_hand: Card = deck.pop_top_of_put_pile()
        
        


    def __cpu_turn(self, deck: Deck):
        pass

    def play_turn(self, deck, last_turn: bool = False):
        if self.player_type == Player.USER_PLAYER:
            self.__user_turn(last_turn)
        elif self.player_type == Player.CPU_PLAYER:
            self.__cpu_turn()

    def update_score(self) -> int:
        """Updates the user's overall score and returns the score for the round"""
        score = self.board.get_score()
        self.score += score
        return score


    