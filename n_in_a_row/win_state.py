import enum
from typing import List, Dict

from n_in_a_row.chip import Chip


class WinState(enum.Enum):

    DRAW = 0
    GREEN = Chip.GREEN.value
    RED = Chip.RED.value

    @staticmethod
    def possible_win_states() -> List['WinState']:
        return [v for _, v in WinState.__members__.items()]


class WinStatesCounter:

    def __init__(self, win_states: Dict[WinState, int]=None):
        self.win_states = win_states
        if self.win_states is None:
            self.win_states = {ws: 0 for ws in WinState.possible_win_states()}

    def __add__(self, other: 'WinStatesCounter') -> 'WinStatesCounter':
        if not isinstance(other, WinStatesCounter):
            raise NotImplemented

        return WinStatesCounter(win_states={
            ws: self.win_states[ws] + other.win_states[ws]
            for ws in WinState.possible_win_states()
        })

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            str({k.name: v for k, v in self.win_states.items()})
        )

    def record_win_state(self, win_state: WinState) -> None:
        if win_state is None:
            return
        self.win_states[win_state] += 1
