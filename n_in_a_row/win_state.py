from __future__ import annotations

import enum
from typing import List

from n_in_a_row.chip import Chip


class WinState(enum.Enum):

    DRAW = 0
    GREEN = Chip.GREEN.value
    RED = Chip.RED.value

    @staticmethod
    def possible_win_states() -> List[WinState]:
        return [v for _, v in WinState.__members__.items()]

    @staticmethod
    def from_chip(chip: Chip) -> WinState:
        if chip == Chip.GREEN:
            return WinState.GREEN
        if chip == Chip.RED:
            return WinState.RED
        if chip == Chip.EMPTY:
            raise ValueError('Chip.EMPTY does not have corresponding WinState')
        raise ValueError(f'Unknown Chip: {chip}')
