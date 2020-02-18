from typing import Optional

from chip import Chip
from game import Game
from solver.game_state import GameState


class Nika:

    def __init__(
            self,
            game: Game,
            next_chip: Chip,
            play_as: Optional[Chip] = None
    ):
        self.root = GameState(game, next_chip)
        self.play_as = play_as
        if self.play_as is None:
            self.play_as = next_chip
        self.leaf_nodes = []

    def _build_next_game_states(self, game_state: GameState):
        if game_state.win_state is not None:
            game_state.propagate_win_state()
            self.leaf_nodes.append(game_state)
            return

        possible_moves = []
        for col in range(game_state.game.grid.cols):
            row = game_state.game.grid.find_empty_row(col)
            if row >= 0:
                possible_moves.append((row, col))

        for move in possible_moves:
            next_game_state = game_state.make_move(move)
            self._build_next_game_states(next_game_state)

    def build_solution_tree(self):
        self._build_next_game_states(self.root)


if __name__ == '__main__':
    nika = Nika(Game(rows_num=2, cols_num=2, chips_in_a_row=2), Chip.GREEN, play_as=Chip.GREEN)

    from time import time

    start = time()
    nika.build_solution_tree()
    end = time()

    print(f'Took {end - start} secs')

    print(nika)
