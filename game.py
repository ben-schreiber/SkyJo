import numpy as np
from player import *
from deck import Deck
from card import Card


class Game:
    def __init__(self, num_players: int, max_score: int):
        self.players = np.array([HumanPlayer(i) for i in range(num_players)])
        self.deck = Deck()
        [_player.init_board(self.deck) for _player in self.players]
        self.max_score = max_score
        self.num_players = num_players

    def run_game(self):
        """Runs an entire game. Until all players other than one pass the score threshold"""
        while np.sum(np.vectorize(Player.get_score)(self.players) < self.max_score) > 1:
            self.one_round()

    def one_round(self):
        """Runs one round of the game"""
        player_to_go_out: int = 0
        not_last_turn = True

        # Play all turns of the round until someone goes out
        while not_last_turn:
            for user in self.players:
                user.play_turn(self.deck)
                if user.went_out():
                    player_to_go_out = user.id
                    not_last_turn = False
                    break

        # Play the last turn for each player who wasn't the one to go out
        for i in range(self.num_players - 1):  # Play the last round
            self.players[(player_to_go_out + 1 + i) % self.num_players].play_turn(
                self.deck, last_turn=True
            )

        # Calculate and update scores accordingly
        scores = np.vectorize(Player.update_score)(self.players)
        if scores[player_to_go_out] != scores.min():
            # If the player to go out didn't have the lowest score, double his score for the round
            self.players[player_to_go_out].score += scores[player_to_go_out]


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser("Input the number of players")

    parser.add_argument("-n", "--num_players", dest="num_players", type=int, default=2)
    parser.add_argument("-s", "--score", dest="score", type=int, default=100)

    args = parser.parse_args()

    game = Game(num_players=args.num_players, max_score=args.score)

    game.run_game()