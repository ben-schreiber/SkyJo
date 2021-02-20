class Player:

    USER_PLAYER = 0
    CPU_PLAYER = 1

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

    def __user_turn(self):
        pass

    def __cpu_turn(self):
        pass

    def play_turn(self, last_turn: bool = False):
        if self.player_type == Player.USER_PLAYER:
            self.__user_turn()
        elif self.player_type == Player.CPU_PLAYER:
            self.__cpu_turn()

    def update_score(self) -> int:
        """Updates the user's overall score and returns the score for the round"""
        score = self.board.get_score()
        self.score += score
        return score


    