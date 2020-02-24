from collections import deque, Counter
from typing import Deque

from n_in_a_row.chip import Chip
from n_in_a_row.grid import Grid
from n_in_a_row.game_state import GameState
from n_in_a_row.game_state_vault import GameStateVault, GameStateNotInVaultError


class GameTreeBuilder:

    def __init__(
            self,
            game_state: GameState
    ):
        self.root = game_state
        self.leaf_node_ids = []

        self.vault = GameStateVault()

    def _build_solution_tree(self) -> None:
        game_states_stack: Deque[GameState] = deque([self.root])
        while game_states_stack:
            game_state = game_states_stack.pop()

            if game_state.win_state is not None:
                game_state_id = self.vault.save_game_state(game_state)
                self.leaf_node_ids.append(game_state_id)
                continue

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
                    self.vault.save_game_state(next_game_state)
                except GameStateNotInVaultError:
                    game_states_stack.append(next_game_state)

            self.vault.save_game_state(game_state)

    def _propagate_leaf_nodes(self) -> None:
        leaf_nodes = self.leaf_nodes
        for game_state, game_state_id in zip(leaf_nodes, self.leaf_node_ids):
            game_state.child_leaf_node_ids.add(game_state_id)

        # FIXME: instead of a queue use parallel regulation to ensure children are always processed before parents
        game_states_queue: Deque[GameState] = deque(leaf_nodes)
        while game_states_queue:
            game_state = game_states_queue.popleft()

            # Add to already present child_leaf_node_ids
            game_state.child_leaf_node_ids.update(
                self.vault.load_game_state(hash(game_state))
                    .child_leaf_node_ids
            )

            self.vault.save_game_state(game_state)

            if not game_state.parents:
                continue
            for parent in game_state.parents:
                parent.child_leaf_node_ids.update(game_state.child_leaf_node_ids)
                game_states_queue.append(parent)

    def _update_win_states_counter(self) -> None:
        self.root = self.vault.load_game_state(hash(self.root))
        game_states_stack: Deque[GameState] = deque([self.root])
        while game_states_stack:
            game_state = game_states_stack.pop()

            win_states = [
                self.vault.load_game_state(game_state_id).win_state
                for game_state_id in game_state.child_leaf_node_ids
            ]
            game_state.win_states_counter = Counter(win_states)
            self.vault.save_game_state(game_state)
            game_states_stack.extend(game_state.children)

    @property
    def leaf_nodes(self):
        return [self.vault.load_game_state(node_id) for node_id in self.leaf_node_ids]

    def build_solution_tree(self) -> None:
        try:
            self.root = self.vault.load_game_state(hash(self.root))
        except GameStateNotInVaultError:
            self._build_solution_tree()
            self._propagate_leaf_nodes()
            self._update_win_states_counter()

            self.root = self.vault.load_game_state(hash(self.root))


if __name__ == '__main__':
    tree_builder = GameTreeBuilder(
        GameState(
            Grid(rows_num=2, cols_num=2),
            next_chip=Chip.GREEN,
            chips_in_a_row=2
        )
    )

    from time import time

    start = time()
    tree_builder.build_solution_tree()
    end = time()

    print(f'Took {end - start} secs')

    print(tree_builder)
