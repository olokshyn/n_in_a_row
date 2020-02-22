from __future__ import annotations

import enum

from n_in_a_row.hashable import Hashable, pack_ints


class Chip(Hashable, enum.Enum):

    EMPTY = 0
    GREEN = 1
    RED = 2

    def build_hash(self, hash_obj) -> None:
        hash_obj.update(pack_ints(self.value))

    def swap_chip(self) -> Chip:
        if self == Chip.EMPTY:
            raise ValueError('Cannot swap empty chip!')
        if self == Chip.GREEN:
            return Chip.RED
        if self == Chip.RED:
            return Chip.GREEN
        raise RuntimeError('Only two chips are supported')
