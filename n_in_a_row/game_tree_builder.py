from typing import Optional

from n_in_a_row.chip import Chip
from n_in_a_row.grid import Grid
from n_in_a_row.game_state import GameState
from n_in_a_row.win_state import WinState
from n_in_a_row.game_state_vault import GameStateVault, GameStateNotInVaultError


class GameTreeBuilder:

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
        self.leaf_node_ids = []

        self.vault = GameStateVault()

    def _build_next_game_states(self, game_state: GameState) -> None:
        if game_state.win_state is not None:
            self.leaf_node_ids.append(hash(game_state))
            return

        possible_moves = []
        for col in range(game_state.grid.cols):
            row = game_state.grid.find_empty_row(col)
            if row >= 0:
                possible_moves.append((row, col))

        for move in possible_moves:
            next_game_state = game_state.make_move(move)
            try:
                next_game_state = self.vault.load_game_state(hash(next_game_state))
                next_game_state.parents.append(game_state)
                self.vault.save_game_state(next_game_state, overwrite=True)
            except GameStateNotInVaultError:
                self._build_next_game_states(next_game_state)

    def _propagate_win_state(self, game_state: GameState, win_state: Optional[WinState] = None) -> None:
        if not game_state.parents:
            return
        if win_state is None:
            win_state = game_state.win_state
        if win_state is None:
            raise ValueError('win_state must be specified')

        for parent in game_state.parents:
            parent.win_states_counter.record_win_state(win_state)
            self.vault.save_game_state(parent, overwrite=True)
            self._propagate_win_state(parent, win_state)

    def build_solution_tree(self) -> None:
        try:
            self.root = self.vault.load_game_state(hash(self.root))
        except GameStateNotInVaultError:
            self._build_next_game_states(self.root)
            self.vault.save_game_state(self.root)

        for leaf_node_id in self.leaf_node_ids:
            self._propagate_win_state(self.vault.load_game_state(leaf_node_id))
        self.leaf_nodes = [self.vault.load_game_state(node_id) for node_id in self.leaf_node_ids]

        self.root = self.vault.load_game_state(hash(self.root))


if __name__ == '__main__':
    nika = GameTreeBuilder(
        GameState(
            Grid(rows_num=2, cols_num=2),
            next_chip=Chip.GREEN,
            chips_in_a_row=2
        )
    )

    from time import time

    start = time()
    nika.build_solution_tree()
    end = time()

    print(f'Took {end - start} secs')

    print(nika)
