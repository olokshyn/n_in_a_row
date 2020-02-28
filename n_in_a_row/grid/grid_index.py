from __future__ import annotations

from n_in_a_row.hashable import Hashable, pack_ints


class GridIndex(Hashable):

    __slots__ = ('row', 'col')

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __iter__(self):
        return iter((self.row, self.col))

    def __repr__(self):
        return f'{self.__class__.__name__}(row={self.row}, col={self.col})'

    def __str__(self):
        return f'({self.row}, {self.col})'

    def __eq__(self, other: GridIndex) -> bool:
        if isinstance(other, GridIndex):
            return self.row == other.row and self.col == other.col
        if isinstance(other, tuple):
            return len(other) == 2 and self.row == other[0] and self.col == other[1]
        return NotImplemented

    def __ne__(self, other: GridIndex) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return super().__hash__()

    def build_hash(self, hash_obj) -> None:
        hash_obj.update(pack_ints(self.row, self.col))
