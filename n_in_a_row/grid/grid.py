from __future__ import annotations

from typing import Tuple, List, Optional, Union

import numpy as np

from n_in_a_row.chip import Chip
from n_in_a_row.win_state import WinState
from n_in_a_row.hashable import Hashable, pack_ints
from n_in_a_row.config import max_grid_shape

from .grid_index import GridIndex
from .cell_union_manager import CellUnionManager


class Grid(Hashable):

    def __init__(self, rows: int, cols: int):
        max_rows, max_cols = max_grid_shape()
        if rows <= 0 or cols <= 0:
            raise ValueError(f'Grid size ({rows}, {cols}), is invalid')
        if rows > max_rows or cols > max_cols:
            raise ValueError(
                f'Grid size ({rows}, {cols}) is greater than the max size ({max_rows}, {max_cols})'
            )

        # Data that defines the grid
        self.rows = rows
        self.cols = cols
        self.grid = np.full((self.rows, self.cols), Chip.EMPTY.value)

        # Derived data used for optimization
        self._unions = {
            'row': CellUnionManager(),
            'col': CellUnionManager(),
            'diag': CellUnionManager(),
            'subdiag': CellUnionManager()
        }
        self._chips_in_cols: List[int] = [0] * self.cols

    def __repr__(self) -> str:
        return '{}(\n{},\nrows={},\ncols={}\n)'.format(
            self.__class__.__name__, repr(self.grid), self.rows, self.cols
        )

    def __setitem__(self, index: Union[GridIndex, Tuple[int, int]], chip: Chip) -> None:
        index = self._check_index(index)
        self._check_chip(chip)
        if self.grid[index.ii] != Chip.EMPTY.value:
            raise CellOccupiedError(index)
        row, col = index
        next_row = row + 1
        if next_row < self.rows and self.grid[next_row, col] == Chip.EMPTY.value:
            raise CellIsDanglingError(index)

        self._set_chip(index, chip)

    def __getitem__(self, index: Union[GridIndex, Tuple[int, int]]) -> Chip:
        index = self._check_index(index)
        return Chip(self.grid[index.ii])

    def build_hash(self, hash_obj) -> None:
        hash_obj.update(pack_ints(self.rows, self.cols))
        hash_obj.update(self.grid.tobytes())

    def find_empty_row(self, col: int) -> int:
        if col < 0 or col >= self.cols:
            raise ValueError(f'Column {col} is out of range')
        return self.rows - self._chips_in_cols[col] - 1

    def drop_chip(self, col: int, chip: Chip) -> None:
        self._check_chip(chip)
        row = self.find_empty_row(col)
        if row < 0:
            raise ColumnFullError(col)
        self._set_chip(GridIndex(row, col), chip)

    def is_full(self) -> bool:
        return all(x == self.rows for x in self._chips_in_cols)

    def get_win_state(self, chips_in_a_row: int) -> Optional[WinState]:
        for unions in self._unions.values():
            index, size = unions.get_max_union_root_and_size()
            if size >= chips_in_a_row:
                return WinState.from_chip(Chip(self.grid[index.ii]))

        if self.is_full():
            return WinState.DRAW

        return None

    def _check_index(self, index: Union[GridIndex, Tuple[int, int]]) -> GridIndex:
        row, col = index
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise IndexError(f'Index {index} is out of bounds')
        if isinstance(index, GridIndex):
            return index
        return GridIndex(row, col)

    @staticmethod
    def _check_chip(chip: Chip) -> None:
        if not isinstance(chip, Chip):
            raise TypeError('Value for Grid must be of type Chip')
        if chip == Chip.EMPTY:
            raise ValueError('Cannot use empty chip')

    def _set_chip(self, index: GridIndex, chip: Chip) -> None:
        self.grid[index.ii] = chip.value
        self._chips_in_cols[index.col] += 1

        row, col = index
        up = row > 0
        down = row < self.rows - 1
        left = col > 0
        right = col < self.cols - 1

        def unite(nrow: int, ncol: int, unions: CellUnionManager):
            neighbor_index = GridIndex(nrow, ncol)
            if self.grid[index.ii] == self.grid[neighbor_index.ii]:
                unions.unite_cells(index, neighbor_index)

        if up:
            unite(row - 1, col, self._unions['col'])
            if left:
                unite(row - 1, col - 1, self._unions['diag'])
            if right:
                unite(row - 1, col + 1, self._unions['subdiag'])
        if left:
            unite(row, col - 1, self._unions['row'])
        if right:
            unite(row, col + 1, self._unions['row'])
        if down:
            unite(row + 1, col, self._unions['col'])
            if left:
                unite(row + 1, col - 1, self._unions['subdiag'])
            if right:
                unite(row + 1, col + 1, self._unions['diag'])


class GridError(RuntimeError):
    pass


class CellError(GridError):

    def __init__(self, index: GridIndex, *args):
        if not args:
            args = [f'Cell {index}']
        super().__init__(*args)
        self.index = index


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
