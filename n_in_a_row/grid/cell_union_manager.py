from __future__ import annotations

from typing import Tuple, Dict, Set, cast

from .grid_index import GridIndex


class CellUnionManager:

    def __init__(self):
        self.parent: Dict[GridIndex, GridIndex] = {}
        self.tree_size: Dict[GridIndex, int] = {}

    def __bool__(self):
        return bool(self.parent)

    def _get_root(self, index: GridIndex) -> GridIndex:
        while index != self.parent[index]:
            self.tree_size[self.parent[index]] -= self.tree_size[index]
            self.parent[index] = self.parent[self.parent[index]]
            index = self.parent[index]
        return index

    def add_cell(self, index: GridIndex) -> None:
        self.parent[index] = index
        self.tree_size[index] = 1

    def are_united(self, left: GridIndex, right: GridIndex) -> bool:
        return self._get_root(left) == self._get_root(right)

    def unite_cells(self, left: GridIndex, right: GridIndex) -> None:
        left_root = self._get_root(left)
        right_root = self._get_root(right)
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
        if not self.tree_size:
            raise NoUnionsError()
        return cast(Tuple[GridIndex, int], max(self.tree_size.items(), key=lambda x: x[1]))

    def get_max_union(self) -> Set[GridIndex]:
        max_root, _ = self.get_max_union_root_and_size()
        return {index for index, parent in self.parent.items() if parent == max_root}


class CellUnionManagerError(Exception):
    pass


class NoUnionsError(CellUnionManagerError):
    pass
