from __future__ import annotations

from copy import deepcopy
from typing import Tuple, Optional

from n_in_a_row.chip import Chip
from n_in_a_row.win_state import WinState, WinStatesCounter
from n_in_a_row.game import Game, GameNotFinishedError, GameFinishedError
from n_in_a_row.hashable import Hashable


class GameState(Hashable):

    def __init__(
            self,
            game: Game,
            next_chip: Chip,
            parent: GameState = None,
            copy_game: bool = True
    ):
        if copy_game:
            self.game = deepcopy(game)
        else:
            self.game = game
        self.next_chip = next_chip

        self.win_states_counter = WinStatesCounter()
        try:
            self.win_state = self.game.get_win_state()
            self.win_states_counter.record_win_state(self.win_state)
        except GameNotFinishedError:
            self.win_state = None

        self.parents = []
        if parent is not None:
            self.parents.append(parent)
        self.children = []

    def __repr__(self) -> str:
        return '{}(\n{},\nnext_chip={},\n' \
               'win_state={},\nwin_states_counter={},' \
               '\nparents={}\nchildren={}\n), hash={}' \
            .format(
                self.__class__.__name__,
                repr(self.game),
                repr(self.next_chip),
                repr(self.win_state),
                repr(self.win_states_counter),
                repr([hash(parent) for parent in self.parents]),
                repr([hash(child) for child in self.children]),
                hash(self)
            )

    def build_hash(self, hash_obj) -> None:
        self.game.build_hash(hash_obj)
        self.next_chip.build_hash(hash_obj)

    def make_move(self, index: Tuple[int, int]) -> GameState:
        if self.win_state is not None:
            raise GameFinishedError()

        game = deepcopy(self.game)
        game.grid[index] = self.next_chip

        child = GameState(
            game=game,
            next_chip=self.next_chip.swap_chip(),
            parent=self,
            copy_game=False
        )
        self.children.append(child)

        return child
