from collections import deque, Counter
from typing import Deque, List, Set

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

    def _build_lower_parallel_regulation(self) -> List[Set[int]]:
        regulation: List[Set[int]] = []
        leaf_nodes = self.get_leaf_nodes()
        next_leaf_nodes = []
        excluded_node_ids: Set[int] = set()
        while leaf_nodes:
            for node in leaf_nodes:
                node_id = hash(node)
                excluded_node_ids.add(node_id)
                for parent in node.parents:
                    parent_children = set(parent.children) - excluded_node_ids
                    if not parent_children:
                        next_leaf_nodes.append(parent)
            regulation.append({hash(node) for node in leaf_nodes})
            leaf_nodes = next_leaf_nodes
            next_leaf_nodes = []
        return regulation

    def _propagate_win_states(self) -> None:
        regulation = self._build_lower_parallel_regulation()
        for level_node_ids in regulation:
            for node_id in level_node_ids:
                node = self.vault.load_game_state(node_id)
                if node.win_state is not None:
                    node.child_leaf_node_ids.add(node_id)
                    win_states = [node.win_state]
                else:
                    for child in node.children:
                        node.child_leaf_node_ids.update(child.child_leaf_node_ids)
                    win_states = [
                        self.vault.load_game_state(game_state_id).win_state
                        for game_state_id in node.child_leaf_node_ids
                    ]
                node.win_states_counter = Counter(win_states)
                self.vault.save_game_state(node)

    def get_leaf_nodes(self):
        return [self.vault.load_game_state(node_id) for node_id in self.leaf_node_ids]

    def build_solution_tree(self) -> None:
        try:
            self.root = self.vault.load_game_state(hash(self.root))
        except GameStateNotInVaultError:
            self._build_solution_tree()
            self._propagate_win_states()

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
