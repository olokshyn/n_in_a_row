from copy import deepcopy
from typing import Tuple

from chip import Chip, swap_chip
from win_state import WinState, WinStatesCounter
from game import Game, GameNotFinishedError, GameFinishedError


class GameState:

    def __init__(
            self,
            game: Game,
            next_chip: Chip,
            parent: 'GameState' = None,
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

        self.parent = parent
        self.children = []

    def __hash__(self):
        return hash(
            # TODO: maybe having multiple parents will allow to reuse child game states?
            # We can get this game state from different parents
            str(hash(self.parent))
            +
            str(hash(self.game))
            +
            str(self.next_chip)
        )

    def make_move(self, index: Tuple[int, int]) -> 'GameState':
        if self.win_state is not None:
            raise GameFinishedError()

        game = deepcopy(self.game)
        game.grid[index] = self.next_chip

        child = GameState(
            game=game,
            next_chip=swap_chip(self.next_chip),
            parent=self,
            copy_game=False
        )
        self.children.append(child)

        return child

    def propagate_win_state(self, win_state: WinState = None) -> None:
        if self.parent is None:
            return
        if win_state is None:
            win_state = self.win_state
        if win_state is None:
            raise ValueError('win_state must be specified')

        self.parent.win_states_counter.record_win_state(win_state)
        self.parent.propagate_win_state(win_state)
