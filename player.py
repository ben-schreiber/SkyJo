class Player:

    def __init__(self, id: int):
        self.id = id
        self.board: Board = None
    
    def get_id(self) -> int:
        return self.id

    def init_board(self, deck: Deck):
        """
        Initializes the player's board with the given deck
        Args:
            deck: The deck (of type Deck) to draw from
        """
        self.board = Board(deck)