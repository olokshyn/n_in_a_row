from typing import Tuple

import numpy as np


from n_in_a_row.chip import Chip
from n_in_a_row.hashable import Hashable, pack_ints


class Grid(Hashable):

    def __init__(self, rows_num: int, cols_num: int):
        self.grid = np.full(
            shape=(rows_num, cols_num),
            fill_value=Chip.EMPTY.value
        )

    def _check_index(self, index: Tuple[int, int]) -> None:
        if len(index) != 2:
            raise TypeError('Use a tuple of length 2 for indexing')
        if (index[0] < 0 or index[0] >= self.rows
                or index[1] < 0 or index[1] >= self.cols):
            raise IndexError(f'Index ({index[0]}, {index[1]}) is out of bounds')

    @staticmethod
    def _check_chip(chip: Chip) -> None:
        if not isinstance(chip, Chip):
            raise TypeError('Value for Grid must be of type Chip')
        if chip == Chip.EMPTY:
            raise ValueError('Cannot use empty chip')

    def __len__(self) -> int:
        return len(self.grid)

    def __iter__(self):
        return iter(self.grid)

    def __repr__(self) -> str:
        return '{}(\n{}\n)'.format(self.__class__.__name__, repr(self.grid))

    def __setitem__(self, key: Tuple[int, int], chip: Chip) -> None:
        self._check_index(key)
        self._check_chip(chip)
        row, col = key
        if self.grid[row, col] != Chip.EMPTY.value:
            raise CellOccupiedError(row=row, col=col)
        next_row = row + 1
        if next_row < len(self.grid) and self.grid[next_row, col] == Chip.EMPTY.value:
            raise CellIsDanglingError(row=row, col=col)
        self.grid[row, col] = chip.value

    def __getitem__(self, index: Tuple[int, int]) -> Chip:
        self._check_index(index)
        row, col = index
        return Chip(self.grid[row, col])

    def __getattr__(self, item):
        attrs_to_skip = {
            '__copy__', '__deepcopy__',
            '__getstate__', '__setstate__'
        }
        if item in attrs_to_skip:
            raise AttributeError()
        return getattr(self.grid, item)

    def build_hash(self, hash_obj) -> None:
        hash_obj.update(pack_ints(*self.grid.shape))
        hash_obj.update(self.grid.data.tobytes())

    @property
    def rows(self) -> int:
        return self.grid.shape[0]

    @property
    def cols(self) -> int:
        return self.grid.shape[1]

    def find_empty_row(self, col: int) -> int:
        if col < 0 or col >= self.cols:
            raise ValueError(f'Column {col} is out of range')
        row = self.rows - 1
        while row >= 0 and self.grid[row, col] != Chip.EMPTY.value:
            row -= 1
        return row

    def drop_chip(self, col: int, chip: Chip) -> None:
        self._check_chip(chip)
        row = self.find_empty_row(col)
        if row < 0:
            raise ColumnFullError(col)
        self.grid[row, col] = chip.value

    def is_full(self) -> bool:
        return np.all(self.grid != Chip.EMPTY.value)


class GridError(RuntimeError):
    pass


class CellError(GridError):

    def __init__(self, row: int, col: int, *args):
        if not args:
            args = [f'Cell ({row}, {col})']
        super().__init__(*args)
        self.row = row
        self.col = col


class CellOccupiedError(CellError):
    pass


class CellIsDanglingError(CellError):
    pass


class ColumnFullError(GridError):

    def __init__(self, col: int, *args):
        if not args:
            args = [f'Column {col} is full']
        super().__init__(*args)
        self.col = col
