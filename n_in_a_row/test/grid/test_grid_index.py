import unittest

import numpy as np

from n_in_a_row.grid.grid_index import GridIndex
from n_in_a_row.config import max_grid_shape


class TestGridIndex(unittest.TestCase):

    def test_config(self):
        max_rows, max_cols = max_grid_shape()
        self.assertEqual(max_rows, GridIndex.MAX_GRID_ROWS)
        self.assertEqual(max_cols, GridIndex.MAX_GRID_COLS)

    def test_init(self):
        self.assertRaises(AssertionError, lambda: GridIndex(-1, 0))
        self.assertRaises(AssertionError, lambda: GridIndex(0, -2))
        self.assertRaises(AssertionError, lambda: GridIndex(-3, -4))
        self.assertRaises(AssertionError, lambda: GridIndex(1, 7))
        self.assertRaises(AssertionError, lambda: GridIndex(6, 4))
        self.assertRaises(AssertionError, lambda: GridIndex(9, 10))
        GridIndex(0, 0)
        GridIndex(2, 3)
        GridIndex(5, 6)

    def test_unpacking(self):
        row, col = GridIndex(1, 2)
        self.assertEqual(1, row)
        self.assertEqual(2, col)

        row, col = GridIndex(5, 6)
        self.assertEqual(5, row)
        self.assertEqual(6, col)

    def test_equality(self):
        self.assertEqual(GridIndex(0, 0), GridIndex(0, 0))
        self.assertEqual(GridIndex(2, 1), GridIndex(2, 1))
        self.assertEqual(GridIndex(4, 6), GridIndex(4, 6))

        self.assertNotEqual(GridIndex(0, 1), GridIndex(0, 0))
        self.assertNotEqual(GridIndex(1, 0), GridIndex(0, 0))
        self.assertNotEqual(GridIndex(2, 1), GridIndex(4, 6))

        self.assertEqual((3, 4), GridIndex(3, 4))
        self.assertEqual(GridIndex(3, 4), (3, 4))

        self.assertNotEqual((1, 2), GridIndex(2, 1))
        self.assertNotEqual(GridIndex(2, 1), (1, 2))
        self.assertNotEqual(GridIndex(2, 3), (2, 3, 4))
        self.assertNotEqual((2, 3, 4), GridIndex(2, 3))
        self.assertNotEqual(GridIndex(0, 0), (0,))
        self.assertNotEqual((0,), GridIndex(0, 0))
        self.assertNotEqual(0, GridIndex(0, 0))
        self.assertNotEqual(GridIndex(0, 0), 0)

    def test_hash(self):
        self.assertEqual(hash(GridIndex(0, 0)), hash(GridIndex(0, 0)))
        self.assertEqual(hash(GridIndex(0, 1)), hash(GridIndex(0, 1)))
        self.assertEqual(hash(GridIndex(1, 0)), hash(GridIndex(1, 0)))
        self.assertEqual(hash(GridIndex(1, 1)), hash(GridIndex(1, 1)))
        self.assertEqual(hash(GridIndex(2, 3)), hash(GridIndex(2, 3)))

        self.assertNotEqual(hash(GridIndex(0, 1)), hash(GridIndex(1, 0)))
        self.assertNotEqual(hash(GridIndex(1, 0)), hash(GridIndex(0, 1)))
        self.assertNotEqual(hash(GridIndex(0, 0)), hash(GridIndex(1, 1)))
        self.assertNotEqual(hash(GridIndex(2, 3)), hash(GridIndex(3, 2)))

    def test_i(self):
        rows, cols = max_grid_shape()
        array = np.arange(rows * cols).reshape((rows, cols))

        self.assertEqual(array[0, 0], GridIndex(0, 0).i)
        self.assertEqual(array[0, 1], GridIndex(0, 1).i)
        self.assertEqual(array[1, 0], GridIndex(1, 0).i)
        self.assertEqual(array[1, 1], GridIndex(1, 1).i)
        self.assertEqual(array[3, 4], GridIndex(3, 4).i)
        self.assertEqual(array[5, 2], GridIndex(5, 2).i)
        self.assertEqual(array[rows - 1, cols - 1], GridIndex(rows - 1, cols - 1).i)

        self.assertEqual((0, 0), GridIndex.from_i(array[0, 0]))
        self.assertEqual((0, 1), GridIndex.from_i(array[0, 1]))
        self.assertEqual((1, 0), GridIndex.from_i(array[1, 0]))
        self.assertEqual((1, 1), GridIndex.from_i(array[1, 1]))
        self.assertEqual((3, 4), GridIndex.from_i(array[3, 4]))
        self.assertEqual((5, 2), GridIndex.from_i(array[5, 2]))
        self.assertEqual((rows - 1, cols - 1), GridIndex.from_i(array[rows - 1, cols - 1]))

    def test_ii(self):
        rows, cols = max_grid_shape()

        self.assertEqual((0, 0), GridIndex(0, 0).ii)
        self.assertEqual((0, 1), GridIndex(0, 1).ii)
        self.assertEqual((1, 0), GridIndex(1, 0).ii)
        self.assertEqual((1, 1), GridIndex(1, 1).ii)
        self.assertEqual((1, 5), GridIndex(1, 5).ii)
        self.assertEqual((3, 2), GridIndex(3, 2).ii)
        self.assertEqual((rows - 1, cols - 1), GridIndex(rows - 1, cols - 1).ii)

        self.assertEqual(GridIndex(0, 0), GridIndex.from_ii((0, 0)))
        self.assertEqual(GridIndex(0, 1), GridIndex.from_ii((0, 1)))
        self.assertEqual(GridIndex(1, 0), GridIndex.from_ii((1, 0)))
        self.assertEqual(GridIndex(1, 1), GridIndex.from_ii((1, 1)))
        self.assertEqual(GridIndex(1, 5), GridIndex.from_ii((1, 5)))
        self.assertEqual(GridIndex(3, 2), GridIndex.from_ii((3, 2)))
        self.assertEqual(GridIndex(rows - 1, cols - 1), GridIndex.from_ii((rows - 1, cols - 1)))


if __name__ == '__main__':
    unittest.main()
