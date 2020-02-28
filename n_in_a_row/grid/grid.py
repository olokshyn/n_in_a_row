from __future__ import annotations

from pickle import dumps
from typing import Tuple, List, Dict, Generator, Optional, Union

from n_in_a_row.chip import Chip
from n_in_a_row.win_state import WinState
from n_in_a_row.hashable import Hashable, pack_ints

from .grid_index import GridIndex
from .cell_union_manager import CellUnionManager


class Grid(Hashable):

    def __init__(self, rows: int, cols: int):
        # Data that defines the grid
        self.rows = rows
        self.cols = cols
        self.grid: Dict[GridIndex, Chip] = {}

        # Derived data used for optimization
        self.unions = CellUnionManager()
        self.chips_in_cols: List[int] = [0] * self.cols

    def __repr__(self) -> str:
        return '{}(\n{},\nrows={},\ncols={}\n)'.format(
            self.__class__.__name__, repr(self.grid), self.rows, self.cols
        )

    def __setitem__(self, index: Union[GridIndex, Tuple[int, int]], chip: Chip) -> None:
        index = self._check_index(index)
        self._check_chip(chip)
        if index in self.grid:
            raise CellOccupiedError(index)
        row, col = index
        next_row = row + 1
        if next_row < self.rows and GridIndex(next_row, col) not in self.grid:
            raise CellIsDanglingError(index)

        self._set_chip(index, chip)

    def __getitem__(self, index: Union[GridIndex, Tuple[int, int]]) -> Chip:
        index = self._check_index(index)
        return self.grid.get(index, Chip.EMPTY)

    def build_hash(self, hash_obj) -> None:
        hash_obj.update(pack_ints(self.rows, self.cols))
        hash_obj.update(dumps(self.grid))

    def find_empty_row(self, col: int) -> int:
        if col < 0 or col >= self.cols:
            raise ValueError(f'Column {col} is out of range')
        return self.rows - self.chips_in_cols[col] - 1

    def drop_chip(self, col: int, chip: Chip) -> None:
        self._check_chip(chip)
        row = self.find_empty_row(col)
        if row < 0:
            raise ColumnFullError(col)
        self._set_chip(GridIndex(row, col), chip)

    def is_full(self) -> bool:
        return all(x == self.rows for x in self.chips_in_cols)

    def get_win_state(self, chips_in_a_row: int) -> Optional[WinState]:
        if not self.unions:
            return None

        index, size = self.unions.get_max_union_root_and_size()
        if size >= chips_in_a_row:
            return WinState.from_chip(self.grid[index])

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

    def _neighbor_cells(self, index: GridIndex) -> Generator[GridIndex]:
        row, col = index
        up = row > 0
        down = row < self.rows - 1
        left = col > 0
        right = col < self.cols - 1

        if up:
            yield row - 1, col
            if left:
                yield GridIndex(row - 1, col - 1)
            if right:
                yield GridIndex(row - 1, col + 1)
        if left:
            yield GridIndex(row, col - 1)
        if right:
            yield GridIndex(row, col + 1)
        if down:
            yield GridIndex(row + 1, col)
            if left:
                yield GridIndex(row + 1, col - 1)
            if right:
                yield GridIndex(row + 1, col + 1)

    def _set_chip(self, index: GridIndex, chip: Chip) -> None:
        self.grid[index] = chip
        self.unions.add_cell(index)
        self.chips_in_cols[index.col] += 1

        for neighbor_index in self._neighbor_cells(index):
            if self.grid[index] == self.grid.get(neighbor_index, Chip.EMPTY):
                self.unions.unite_cells(index, neighbor_index)


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
