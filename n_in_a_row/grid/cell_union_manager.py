from __future__ import annotations

from typing import Tuple, cast

import numpy as np

from n_in_a_row.config import max_grid_shape

from .grid_index import GridIndex


class CellUnionManager:

    def __init__(self):
        max_rows, max_cols = max_grid_shape()
        array_size = max_rows * max_cols
        self.parent = np.arange(array_size)
        # tree size is valid only for roots
        self.tree_size = np.ones(array_size)

    def _get_root(self, index_i: int) -> int:
        while index_i != self.parent[index_i]:
            # we don't need to update size for non-root nodes
            # if self.parent[index_i] != self.parent[self.parent[index_i]]:
            #     self.tree_size[self.parent[index_i]] -= self.tree_size[index_i]
            self.parent[index_i] = self.parent[self.parent[index_i]]
            index_i = self.parent[index_i]
        return index_i

    def are_united(self, left: GridIndex, right: GridIndex) -> bool:
        return self._get_root(left.i) == self._get_root(right.i)

    def unite_cells(self, left: GridIndex, right: GridIndex) -> None:
        left_root = self._get_root(left.i)
        right_root = self._get_root(right.i)
        if left_root == right_root:
            return
        left_size = self.tree_size[left_root]
        right_size = self.tree_size[right_root]
        if left_size >= right_size:
            self.parent[right_root] = left_root
            self.tree_size[left_root] += self.tree_size[right_root]
        else:
            self.parent[left_root] = right_root
            self.tree_size[right_root] += self.tree_size[left_root]

    def get_max_union_root_and_size(self) -> Tuple[GridIndex, int]:
        max_root = cast(int, np.argmax(self.tree_size))
        return GridIndex.from_i(max_root), self.tree_size[max_root]


class CellUnionManagerError(Exception):
    pass


class NoUnionsError(CellUnionManagerError):
    pass
