from player import Player
from deck import Deck
from card import Card


class Game:

    def __init__(self, num_players: int, max_score: int):
        self.players = [Player(i) for i in range(num_players)]
        self.max_score = max_score

    def run_game(self):
        """Runs an entire game. Until all players other than one pass the score threshold"""
        pass

    def one_round(self):
        """Runs one round of the game"""
        pass




if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser('Input the number of players')

    parser.add_argument('-n', '--num_players', dest='num_players', type=int, default=2)
    parser.add_argument('-s', '--score', dest='score', type=int, default=100)

    args = parser.parse_args()

    game = Game(
        num_players = args.num_players,
        max_score = args.score
        )

    game.run_game()