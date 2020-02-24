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

