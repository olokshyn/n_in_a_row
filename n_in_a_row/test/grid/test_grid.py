import unittest

from n_in_a_row.grid import grid
from n_in_a_row.chip import Chip
from n_in_a_row.win_state import WinState
from n_in_a_row.config import max_grid_shape


class TestInit(unittest.TestCase):

    def test_ok(self):
        max_rows, max_cols = max_grid_shape()
        g = grid.Grid(rows=max_rows, cols=max_cols)
        for i in range(max_rows):
            for j in range(max_cols):
                self.assertEqual(Chip.EMPTY, g[i, j])
        self.assertEqual(max_rows, g.rows)
        self.assertEqual(max_cols, g.cols)

    def test_invalid(self):
        self.assertRaises(ValueError, lambda: grid.Grid(rows=0, cols=0))
        self.assertRaises(ValueError, lambda: grid.Grid(rows=-1, cols=3))
        self.assertRaises(ValueError, lambda: grid.Grid(rows=2, cols=-3))
        self.assertRaises(ValueError, lambda: grid.Grid(rows=-1, cols=-3))

        rows, cols = max_grid_shape()
        self.assertRaises(ValueError, lambda: grid.Grid(rows=rows + 1, cols=cols + 1))
        self.assertRaises(ValueError, lambda: grid.Grid(rows=3, cols=cols + 1))
        self.assertRaises(ValueError, lambda: grid.Grid(rows=rows + 1, cols=cols + 1))


class TestSetterGetter(unittest.TestCase):

    def test_out_of_bounds_index(self):
        g = grid.Grid(rows=6, cols=5)
        self.assertRaises(IndexError, lambda: g[6, 5])
        self.assertRaises(IndexError, lambda: g[0, 5])
        self.assertRaises(IndexError, lambda: g[6, 4])
        self.assertRaises(IndexError, lambda: g[-1, 2])
        self.assertRaises(IndexError, lambda: g[3, -2])
        self.assertRaises(IndexError, lambda: g[-3, -2])
        self.assertRaises(IndexError, lambda: g[2, 6])
        self.assertRaises(IndexError, lambda: g[7, 3])

        self.assertRaises(TypeError, lambda: g[3])

    def test_set(self):
        rows, cols = max_grid_shape()
        g = grid.Grid(rows=rows, cols=cols)
        for i in range(rows - 1, -1, -1):
            for j in range(cols):
                g[i, j] = Chip.GREEN if j % 2 == 0 else Chip.RED

        for i in range(rows - 1, -1, -1):
            for j in range(cols):
                self.assertEqual(g[i, j], Chip.GREEN if j % 2 == 0 else Chip.RED)

    def test_out_of_bounds_set(self):
        g = grid.Grid(rows=3, cols=4)

        def do_assign(row, col):
            g[row, col] = Chip.GREEN

        self.assertRaises(IndexError, do_assign, 3, 4)
        self.assertRaises(IndexError, do_assign, 0, 6)
        self.assertRaises(IndexError, do_assign, 3, 2)
        self.assertRaises(IndexError, do_assign, -1, 3)
        self.assertRaises(IndexError, do_assign, 2, -2)
        self.assertRaises(IndexError, do_assign, -2, -2)

    def test_invalid_value_set(self):
        g = grid.Grid(rows=6, cols=7)

        def do_assign(row, col, value):
            g[row, col] = value

        self.assertRaises(TypeError, do_assign, 5, 0, 0)
        self.assertRaises(TypeError, do_assign, 5, 0, Chip.GREEN.value)
        self.assertRaises(TypeError, do_assign, 5, 0, Chip.RED.value)
        self.assertRaises(TypeError, do_assign, 5, 0, Chip.EMPTY.value)
        self.assertRaises(TypeError, do_assign, 5, 0, 'GREEN')
        self.assertRaises(TypeError, do_assign, 5, 0, None)

        self.assertRaises(ValueError, do_assign, 5, 1, Chip.EMPTY)
        self.assertRaises(ValueError, do_assign, 5, 2, Chip.EMPTY)

    def test_invalid_cell_set(self):
        g = grid.Grid(rows=4, cols=3)

        def do_assign(row, col, value):
            g[row, col] = value

        self.assertRaises(grid.CellIsDanglingError, do_assign, 0, 0, Chip.GREEN)
        self.assertRaises(grid.CellIsDanglingError, do_assign, 0, 1, Chip.RED)
        self.assertRaises(grid.CellIsDanglingError, do_assign, 0, 2, Chip.GREEN)
        self.assertRaises(grid.CellIsDanglingError, do_assign, 1, 0, Chip.RED)
        self.assertRaises(grid.CellIsDanglingError, do_assign, 1, 1, Chip.GREEN)
        self.assertRaises(grid.CellIsDanglingError, do_assign, 1, 2, Chip.RED)
        self.assertRaises(grid.CellIsDanglingError, do_assign, 2, 0, Chip.GREEN)
        self.assertRaises(grid.CellIsDanglingError, do_assign, 2, 1, Chip.RED)
        self.assertRaises(grid.CellIsDanglingError, do_assign, 2, 2, Chip.GREEN)

        g[3, 0] = Chip.RED
        g[3, 1] = Chip.GREEN
        g[3, 2] = Chip.RED

        g[2, 0] = Chip.GREEN
        g[2, 1] = Chip.RED
        g[2, 2] = Chip.GREEN

        self.assertEqual(Chip.RED, g[3, 0])
        self.assertEqual(Chip.GREEN, g[3, 1])
        self.assertEqual(Chip.RED, g[3, 2])
        self.assertEqual(Chip.GREEN, g[2, 0])
        self.assertEqual(Chip.RED, g[2, 1])
        self.assertEqual(Chip.GREEN, g[2, 2])

        self.assertRaises(grid.CellOccupiedError, do_assign, 3, 0, Chip.RED)
        self.assertRaises(grid.CellOccupiedError, do_assign, 3, 1, Chip.RED)
        self.assertRaises(grid.CellOccupiedError, do_assign, 3, 2, Chip.GREEN)
        self.assertRaises(grid.CellOccupiedError, do_assign, 2, 0, Chip.RED)
        self.assertRaises(grid.CellOccupiedError, do_assign, 2, 1, Chip.GREEN)
        self.assertRaises(grid.CellOccupiedError, do_assign, 2, 2, Chip.GREEN)


class TestHash(unittest.TestCase):

    def test_empty_grids(self):
        g1 = grid.Grid(rows=3, cols=2)
        g2 = grid.Grid(rows=3, cols=2)
        self.assertEqual(hash(g1), hash(g2))

    def test_same_grids(self):
        g1 = grid.Grid(rows=3, cols=3)
        g1.drop_chip(0, Chip.RED)
        g1.drop_chip(0, Chip.GREEN)
        g1.drop_chip(1, Chip.RED)
        g1.drop_chip(1, Chip.GREEN)
        g1.drop_chip(1, Chip.GREEN)
        g1.drop_chip(2, Chip.RED)
        g1.drop_chip(2, Chip.GREEN)

        g2 = grid.Grid(rows=3, cols=3)
        g2.drop_chip(0, Chip.RED)
        g2.drop_chip(0, Chip.GREEN)
        g2.drop_chip(1, Chip.RED)
        g2.drop_chip(1, Chip.GREEN)
        g2.drop_chip(1, Chip.GREEN)
        g2.drop_chip(2, Chip.RED)
        g2.drop_chip(2, Chip.GREEN)

        self.assertEqual(hash(g1), hash(g2))

    def test_same_grids_diff_created(self):
        g1 = grid.Grid(rows=2, cols=3)
        g1.drop_chip(0, Chip.GREEN)
        g1.drop_chip(1, Chip.RED)
        g1.drop_chip(2, Chip.GREEN)

        g2 = grid.Grid(rows=2, cols=3)
        g2.drop_chip(2, Chip.GREEN)
        g2.drop_chip(1, Chip.RED)
        g2.drop_chip(0, Chip.GREEN)

        self.assertEqual(hash(g1), hash(g2))

    def test_diff_grids(self):
        g1 = grid.Grid(rows=2, cols=3)
        g1.drop_chip(0, Chip.GREEN)
        g1.drop_chip(1, Chip.RED)
        g1.drop_chip(2, Chip.GREEN)

        g2 = grid.Grid(rows=2, cols=3)
        g2.drop_chip(0, Chip.GREEN)
        g2.drop_chip(1, Chip.GREEN)
        g2.drop_chip(2, Chip.GREEN)

        self.assertNotEqual(hash(g1), hash(g2))

        g1 = grid.Grid(rows=2, cols=3)
        g1.drop_chip(0, Chip.GREEN)
        g1.drop_chip(1, Chip.RED)

        g2 = grid.Grid(rows=2, cols=3)
        g2.drop_chip(1, Chip.RED)
        g2.drop_chip(2, Chip.GREEN)

        self.assertNotEqual(hash(g1), hash(g2))

    def test_same_content_diff_size(self):
        g1 = grid.Grid(rows=3, cols=3)
        g1.drop_chip(0, Chip.GREEN)
        g1.drop_chip(1, Chip.RED)
        g1.drop_chip(2, Chip.GREEN)

        g2 = grid.Grid(rows=2, cols=3)
        g2.drop_chip(0, Chip.GREEN)
        g2.drop_chip(1, Chip.RED)
        g2.drop_chip(2, Chip.GREEN)

        self.assertNotEqual(hash(g1), hash(g2))

        g1 = grid.Grid(rows=2, cols=3)
        g1.drop_chip(0, Chip.GREEN)
        g1.drop_chip(1, Chip.RED)
        g1.drop_chip(2, Chip.GREEN)

        g2 = grid.Grid(rows=2, cols=4)
        g2.drop_chip(0, Chip.GREEN)
        g2.drop_chip(1, Chip.RED)
        g2.drop_chip(2, Chip.GREEN)

        self.assertNotEqual(hash(g1), hash(g2))


class TestFindEmptyRow(unittest.TestCase):

    def test_empty_grid(self):
        rows, cols = max_grid_shape()
        g = grid.Grid(rows=rows, cols=cols)

        for col in range(cols):
            self.assertEqual(rows - 1, g.find_empty_row(col))

    def test_full_grid(self):
        rows, cols = max_grid_shape()
        g = grid.Grid(rows=rows, cols=cols)

        for i in range(rows - 1, -1, -1):
            for j in range(cols):
                g[i, j] = Chip.GREEN

        for col in range(cols):
            self.assertEqual(-1, g.find_empty_row(col))

    def test_various_grid(self):
        g = grid.Grid(rows=5, cols=6)

        g[4, 0] = Chip.GREEN
        g[3, 0] = Chip.RED
        g[2, 0] = Chip.GREEN
        g[1, 0] = Chip.GREEN
        g[0, 0] = Chip.GREEN
        self.assertEqual(-1, g.find_empty_row(0))

        g[4, 1] = Chip.RED
        g[3, 1] = Chip.RED
        g[2, 1] = Chip.RED
        g[1, 1] = Chip.RED
        self.assertEqual(0, g.find_empty_row(1))

        g[4, 2] = Chip.GREEN
        g[3, 2] = Chip.GREEN
        g[2, 2] = Chip.RED
        self.assertEqual(1, g.find_empty_row(2))

        g[4, 3] = Chip.GREEN
        g[3, 3] = Chip.RED
        self.assertEqual(2, g.find_empty_row(3))

        g[4, 4] = Chip.RED
        self.assertEqual(3, g.find_empty_row(4))

        self.assertEqual(4, g.find_empty_row(5))


class TestDropChip(unittest.TestCase):

    def test_empty_grid(self):
        g = grid.Grid(rows=6, cols=5)

        for col in range(5):
            g.drop_chip(col, Chip.GREEN)

        for col in range(5):
            self.assertEqual(Chip.GREEN, g[5, col])

            for row in range(5):
                self.assertEqual(Chip.EMPTY, g[row, col])

    def test_full_grid(self):
        g = grid.Grid(rows=3, cols=3)

        for i in range(2, -1, -1):
            for j in range(3):
                g[i, j] = Chip.GREEN

        for col in range(3):
            self.assertRaises(grid.ColumnFullError, g.drop_chip, col, Chip.RED)

        for i in range(3):
            for j in range(3):
                self.assertEqual(Chip.GREEN, g[i, j])

    def test_various_grid(self):
        g = grid.Grid(rows=5, cols=6)

        g[4, 0] = Chip.GREEN
        g[3, 0] = Chip.RED
        g[2, 0] = Chip.GREEN
        g[1, 0] = Chip.GREEN
        g[0, 0] = Chip.GREEN
        self.assertRaises(grid.ColumnFullError, g.drop_chip, 0, Chip.RED)
        self.assertEqual(Chip.GREEN, g[0, 0])

        g[4, 1] = Chip.RED
        g[3, 1] = Chip.RED
        g[2, 1] = Chip.RED
        g[1, 1] = Chip.RED
        g.drop_chip(1, Chip.GREEN)
        self.assertEqual(Chip.RED, g[1, 1])
        self.assertEqual(Chip.GREEN, g[0, 1])

        g[4, 2] = Chip.GREEN
        g[3, 2] = Chip.GREEN
        g[2, 2] = Chip.RED
        g.drop_chip(2, Chip.GREEN)
        self.assertEqual(Chip.RED, g[2, 2])
        self.assertEqual(Chip.GREEN, g[1, 2])
        self.assertEqual(Chip.EMPTY, g[0, 2])

        g[4, 3] = Chip.GREEN
        g[3, 3] = Chip.RED
        g.drop_chip(3, Chip.GREEN)
        self.assertEqual(Chip.RED, g[3, 3])
        self.assertEqual(Chip.GREEN, g[2, 3])
        self.assertEqual(Chip.EMPTY, g[1, 3])
        self.assertEqual(Chip.EMPTY, g[0, 3])

        g[4, 4] = Chip.RED
        g.drop_chip(4, Chip.GREEN)
        self.assertEqual(Chip.RED, g[4, 4])
        self.assertEqual(Chip.GREEN, g[3, 4])
        self.assertEqual(Chip.EMPTY, g[2, 4])
        self.assertEqual(Chip.EMPTY, g[1, 4])
        self.assertEqual(Chip.EMPTY, g[0, 4])

        g.drop_chip(5, Chip.GREEN)
        self.assertEqual(Chip.GREEN, g[4, 5])
        self.assertEqual(Chip.EMPTY, g[3, 5])
        self.assertEqual(Chip.EMPTY, g[2, 5])
        self.assertEqual(Chip.EMPTY, g[1, 5])
        self.assertEqual(Chip.EMPTY, g[0, 5])


class TestIsFull(unittest.TestCase):

    def test(self):
        g = grid.Grid(rows=6, cols=5)
        self.assertFalse(g.is_full())

        g[5, 1] = Chip.GREEN
        self.assertFalse(g.is_full())

        g[5, 0] = Chip.RED
        g[5, 2] = Chip.RED
        g[5, 3] = Chip.RED
        g.drop_chip(4, Chip.GREEN)
        self.assertFalse(g.is_full())

        for i in range(5):
            for j in range(5):
                g.drop_chip(j, Chip.GREEN)
        self.assertTrue(g.is_full())


class TestGetWinState(unittest.TestCase):

    def test_no_win_state(self):
        g = grid.Grid(rows=4, cols=3)
        self.assertIsNone(g.get_win_state(4))

        g.drop_chip(0, Chip.RED)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.RED)
        self.assertIsNone(g.get_win_state(4))

        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.GREEN)
        self.assertIsNone(g.get_win_state(4))

        g.drop_chip(0, Chip.RED)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.RED)

        self.assertIsNone(g.get_win_state(4))

    def test_draw(self):
        g = grid.Grid(rows=4, cols=4)

        g.drop_chip(0, Chip.RED)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.RED)
        g.drop_chip(3, Chip.GREEN)

        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.RED)

        g.drop_chip(0, Chip.RED)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.RED)
        g.drop_chip(3, Chip.GREEN)

        g.drop_chip(0, Chip.RED)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.RED)
        g.drop_chip(3, Chip.GREEN)

        self.assertEqual(WinState.DRAW, g.get_win_state(4))

    def test_win_in_a_row(self):
        g = grid.Grid(rows=1, cols=4)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.GREEN)
        self.assertEqual(WinState.GREEN, g.get_win_state(3))
        self.assertEqual(WinState.GREEN, g.get_win_state(4))

        g = grid.Grid(rows=2, cols=4)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.RED)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(3, Chip.GREEN)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.GREEN)
        self.assertEqual(WinState.GREEN, g.get_win_state(3))
        self.assertEqual(WinState.GREEN, g.get_win_state(4))

    def test_win_in_a_col(self):
        g = grid.Grid(rows=4, cols=1)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(0, Chip.GREEN)
        self.assertEqual(WinState.GREEN, g.get_win_state(3))
        self.assertEqual(WinState.GREEN, g.get_win_state(4))

        g = grid.Grid(rows=4, cols=2)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(0, Chip.RED)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(0, Chip.RED)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(1, Chip.GREEN)
        self.assertEqual(WinState.GREEN, g.get_win_state(3))
        self.assertEqual(WinState.GREEN, g.get_win_state(4))

    def test_win_in_row_and_col(self):
        g = grid.Grid(rows=4, cols=4)
        g.drop_chip(0, Chip.RED)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.RED)

        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.GREEN)

        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(2, Chip.GREEN)

        self.assertEqual(WinState.GREEN, g.get_win_state(4))

    def test_win_in_a_diag(self):
        g = grid.Grid(rows=4, cols=4)

        g.drop_chip(0, Chip.RED)
        g.drop_chip(0, Chip.RED)
        g.drop_chip(0, Chip.RED)
        g.drop_chip(0, Chip.GREEN)

        g.drop_chip(1, Chip.RED)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(1, Chip.GREEN)

        g.drop_chip(2, Chip.RED)
        g.drop_chip(2, Chip.GREEN)

        g.drop_chip(3, Chip.GREEN)

        self.assertEqual(WinState.GREEN, g.get_win_state(4))

    def test_win_in_a_subdiag(self):
        g = grid.Grid(rows=4, cols=4)

        g.drop_chip(0, Chip.GREEN)

        g.drop_chip(1, Chip.RED)
        g.drop_chip(1, Chip.GREEN)

        g.drop_chip(2, Chip.RED)
        g.drop_chip(2, Chip.RED)
        g.drop_chip(2, Chip.GREEN)

        g.drop_chip(3, Chip.RED)
        g.drop_chip(3, Chip.RED)
        g.drop_chip(3, Chip.RED)
        g.drop_chip(3, Chip.GREEN)

        self.assertEqual(WinState.GREEN, g.get_win_state(4))

    def test_win_in_two_diags(self):
        g = grid.Grid(rows=4, cols=5)

        g.drop_chip(0, Chip.RED)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.GREEN)
        g.drop_chip(4, Chip.RED)

        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.RED)
        g.drop_chip(4, Chip.GREEN)

        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.RED)
        g.drop_chip(3, Chip.GREEN)

        g.drop_chip(1, Chip.RED)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.RED)


if __name__ == '__main__':
    unittest.main()
