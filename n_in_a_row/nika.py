from typing import Optional

from n_in_a_row.chip import Chip
from n_in_a_row.game import Game
from n_in_a_row.game_state import GameState
from n_in_a_row.game_state_vault import GameStateVault, GameStateNotInVaultError


class Nika:

    def __init__(
            self,
            game_state: GameState,
            play_as: Optional[Chip] = None
    ):
        self.root = game_state
        self.play_as = play_as
        if self.play_as is None:
            self.play_as = game_state.next_chip
        self.leaf_nodes = []

        self.vault = GameStateVault()

    def _build_next_game_states(self, game_state: GameState) -> None:
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

    def build_solution_tree(self) -> None:
        try:
            self.root = self.vault.load_game_state(hash(self.root))
        except GameStateNotInVaultError:
            self._build_next_game_states(self.root)
            self.vault.save_game_state(self.root)


if __name__ == '__main__':
    nika = Nika(
        GameState(
            Game(rows_num=3, cols_num=2, chips_in_a_row=2),
            next_chip=Chip.GREEN
        )
    )

    from time import time

    start = time()
    nika.build_solution_tree()
    end = time()

    print(f'Took {end - start} secs')

    print(nika)
