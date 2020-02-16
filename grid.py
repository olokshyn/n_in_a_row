from typing import Tuple

import numpy as np


from chip import Chip


class Grid:

    def __init__(self, rows_num: int, col_num: int):
        self.grid = np.full(
            shape=(rows_num, col_num),
            fill_value=Chip.EMPTY.value
        )

    def _check_index(self, index: Tuple[int, int]):
        if len(index) != 2:
            raise ValueError('Use a tuple of length 2 for indexing')
        if (index[0] < 0 or index[0] >= self.grid.shape[0]
                or index[1] < 0 or index[1] >= self.grid.shape[1]):
            raise ValueError(f'Index ({index[0]}, {index[1]}) is out of bounds')

    def _check_chip(self, chip: Chip):
        if chip == Chip.EMPTY:
            raise ValueError('Cannot use empty chip')

    def __repr__(self):
        return repr(self.grid)

    def __setitem__(self, key: Tuple[int, int], chip: Chip):
        self._check_index(key)
        self._check_chip(chip)
        row, col = key
        if self.grid[row, col] != Chip.EMPTY.value:
            raise CellOccupiedError(row=row, col=col)
        next_row = row + 1
        if next_row < len(self.grid) and self.grid[next_row, col] == Chip.EMPTY.value:
            raise CellIsDanglingError(row=row, col=col)
        self.grid[row, col] = chip.value

    def __getitem__(self, index: Tuple[int, int]):
        self._check_index(index)
        row, col = index
        return Chip(self.grid[row, col])

    def drop_chip(self, col: int, chip: Chip):
        if col < 0 or col >= self.grid.shape[1]:
            raise ValueError(f'Column {col} is out of range')
        self._check_chip(chip)
        row = self.grid.shape[0] - 1
        while row >= 0 and self.grid[row, col] != Chip.EMPTY.value:
            row -= 1
        if row < 0:
            raise ColumnFullError(col)
        self.grid[row, col] = chip.value


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
