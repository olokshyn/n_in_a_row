from __future__ import annotations

from typing import Tuple

from n_in_a_row.config import load_config


class GridIndexMeta(type):

    def __new__(cls, *args, **kwargs):
        clsobj = super().__new__(cls, *args, **kwargs)
        config = load_config()
        clsobj.MAX_GRID_ROWS = config['max_grid_rows']
        clsobj.MAX_GRID_COLS = config['max_grid_cols']
        return clsobj


class GridIndex(metaclass=GridIndexMeta):

    MAX_GRID_ROWS = None
    MAX_GRID_COLS = None

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
        return self.row * self.MAX_GRID_COLS + self.col

    @property
    def i(self) -> int:
        return self.row * self.MAX_GRID_COLS + self.col

    @classmethod
    def from_i(cls, i: int) -> GridIndex:
        return GridIndex(i // cls.MAX_GRID_COLS, i % cls.MAX_GRID_COLS)

    @property
    def ii(self) -> Tuple[int, int]:
        return self.row, self.col

    @classmethod
    def from_ii(cls, ii: Tuple[int, int]) -> GridIndex:
        return GridIndex(ii[0], ii[1])
