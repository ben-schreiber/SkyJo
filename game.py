import numpy as np
from player import *
from pile import PutPile, DrawPile
import abc
from typing import Iterable


class Round:
    def __init__(self, players: Iterable[Player]):
        pass

    def play_round(self):
        pass


class Game(abc.ABC):

    def __init__(self, num_players: int, max_score: int):
        self.max_score = max_score
        self.num_players = num_players
        self.draw_pile = DrawPile()
        self.put_pile = PutPile()
        self.players = tuple(HumanPlayer(i) for i in range(num_players))
         

    def run_game(self):
        """
        Runs an entire game. Until all players other than one pass the score threshold
        """
        remaining_players = [player for player in self.players if player.score < self.max_score]
        while len(remaining_players) > 1:
            r = Round(remaining_players)
            r.play_round()
            remaining_players = [player for player in remaining_players if player.score < self.max_score]

    @abc.abstractmethod
    def one_round(self):
        """
        Runs one round of the game
        """
        pass


class CLIGame(Game):  

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
    parser.add_argument("--num_human_players", dest="human_players", type=int, default=None)
    parser.add_argument("-i", "--interface", dest="interface", type=str, default="cli")

    args = parser.parse_args()
    if args.human_players is None:
        args.human_players = args.num_players

    if args.interface == "cli":
        game = CLIGame(args.num_players, args.score, args.human_players)
    elif args.interface == "gui":
        pass
    else:
        raise ValueError(f"The interface type {args.interface} is invalid. Please try again")

    game.run_game()