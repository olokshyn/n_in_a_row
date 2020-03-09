from __future__ import annotations

from copy import deepcopy
from functools import cached_property
from typing import Optional, List, Dict, Set

from n_in_a_row.chip import Chip
from n_in_a_row.grid import Grid, GridIndex
from n_in_a_row.win_state import WinState
from n_in_a_row.hashable import Hashable, pack_ints


class GameState(Hashable):

    def __init__(
            self,
            grid: Grid,
            next_chip: Chip,
            chips_in_a_row: int,
            parent: Optional[GameState] = None,
            copy_grid: bool = True
    ):
        if copy_grid:
            self.grid = deepcopy(grid)
        else:
            self.grid = grid
        self.next_chip = next_chip
        self.chips_in_a_row = chips_in_a_row

        self.win_state = self.grid.get_win_state(self.chips_in_a_row)

        self.win_states_counter: Optional[Dict[WinState, int]] = None

        self.parents: List[GameState] = []
        if parent is not None:
            self.parents.append(parent)
        self.children: List[GameState] = []
        self.child_leaf_node_ids: Set[int] = set()

    def __repr__(self) -> str:
        return '{}(\n{},\nnext_chip={},\nchips_in_a_row={},\n' \
               'win_state={},\nwin_states_counter={},' \
               '\nparents={}\nchildren={}\n), game_state_id={}' \
            .format(
                self.__class__.__name__,
                repr(self.grid),
                repr(self.next_chip),
                repr(self.chips_in_a_row),
                repr(self.win_state),
                repr(self.win_states_counter),
                repr([parent.game_state_id for parent in self.parents]),
                repr([child.game_state_id for child in self.children]),
                self.game_state_id
            )

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return NotImplemented
        return (
            self.grid == other.grid
            and self.next_chip == other.next_chip
            and self.chips_in_a_row == other.chips_in_a_row
            and self.win_state == other.win_state
        )

    def __hash__(self) -> int:
        return super().__hash__()

    @cached_property
    def game_state_id(self) -> int:
        return hash(self)

    def build_hash(self, hash_obj) -> None:
        self.grid.build_hash(hash_obj)
        self.next_chip.build_hash(hash_obj)
        hash_obj.update(pack_ints(self.chips_in_a_row))

    def make_move(self, index: GridIndex) -> GameState:
        if self.win_state is not None:
            raise GameFinishedError()

        grid = deepcopy(self.grid)
        grid[index] = self.next_chip

        child = GameState(
            grid=grid,
            next_chip=self.next_chip.swap_chip(),
            chips_in_a_row=self.chips_in_a_row,
            parent=self,
            copy_grid=False
        )
        self.children.append(child)

        return child


class GameError(Exception):
    pass


class GameFinishedError(GameError):
    pass
