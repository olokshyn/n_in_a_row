from unittest import TestCase

import grid
from chip import Chip


class TestSetterGetter(TestCase):

    def test_default_initialized(self):
        g = grid.Grid(5, 7)
        for i in range(5):
            for j in range(7):
                self.assertEqual(Chip.EMPTY, g[i, j])

    def test_out_of_bounds_index(self):
        g = grid.Grid(7, 6)
        self.assertRaises(IndexError, lambda: g[7, 6])
        self.assertRaises(IndexError, lambda: g[0, 6])
        self.assertRaises(IndexError, lambda: g[7, 5])
        self.assertRaises(IndexError, lambda: g[-1, 2])
        self.assertRaises(IndexError, lambda: g[3, -2])
        self.assertRaises(IndexError, lambda: g[-3, -2])
        self.assertRaises(IndexError, lambda: g[2, 7])
        self.assertRaises(IndexError, lambda: g[8, 3])

        self.assertRaises(TypeError, lambda: g[3])

    def test_set(self):
        g = grid.Grid(12, 8)
        for i in range(11, -1, -1):
            for j in range(8):
                g[i, j] = Chip.GREEN if j % 2 == 0 else Chip.RED

        for i in range(11, -1, -1):
            for j in range(8):
                self.assertEqual(g[i, j], Chip.GREEN if j % 2 == 0 else Chip.RED)

    def test_out_of_bounds_set(self):
        g = grid.Grid(3, 4)

        def do_assign(row, col):
            g[row, col] = Chip.GREEN

        self.assertRaises(IndexError, do_assign, 3, 4)
        self.assertRaises(IndexError, do_assign, 0, 6)
        self.assertRaises(IndexError, do_assign, 3, 2)
        self.assertRaises(IndexError, do_assign, -1, 3)
        self.assertRaises(IndexError, do_assign, 2, -2)
        self.assertRaises(IndexError, do_assign, -2, -2)

    def test_invalid_value_set(self):
        g = grid.Grid(6, 7)

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
        g = grid.Grid(4, 3)

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


class TestFindEmptyRow(TestCase):

    def test_empty_grid(self):
        g = grid.Grid(10, 12)

        for col in range(12):
            self.assertEqual(9, g.find_empty_row(col))

    def test_full_grid(self):
        g = grid.Grid(10, 12)

        for i in range(9, -1, -1):
            for j in range(12):
                g[i, j] = Chip.GREEN

        for col in range(12):
            self.assertEqual(-1, g.find_empty_row(col))

    def test_various_grid(self):
        g = grid.Grid(5, 6)

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


class TestDropChip(TestCase):

    def test_empty_grid(self):
        g = grid.Grid(8, 5)

        for col in range(5):
            g.drop_chip(col, Chip.GREEN)

        for col in range(5):
            self.assertEqual(Chip.GREEN, g[7, col])

            for row in range(7):
                self.assertEqual(Chip.EMPTY, g[row, col])

    def test_full_grid(self):
        g = grid.Grid(3, 3)

        for i in range(2, -1, -1):
            for j in range(3):
                g[i, j] = Chip.GREEN

        for col in range(3):
            self.assertRaises(grid.ColumnFullError, g.drop_chip, col, Chip.RED)

        for i in range(3):
            for j in range(3):
                self.assertEqual(Chip.GREEN, g[i, j])

    def test_various_grid(self):
        g = grid.Grid(5, 6)

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


class TestIsFull(TestCase):

    def test(self):
        g = grid.Grid(8, 5)
        self.assertFalse(g.is_full())

        g[7, 1] = Chip.GREEN
        self.assertFalse(g.is_full())

        g[7, 0] = Chip.RED
        g[7, 2] = Chip.RED
        g[7, 3] = Chip.RED
        g.drop_chip(4, Chip.GREEN)
        self.assertFalse(g.is_full())

        for i in range(7):
            for j in range(5):
                g.drop_chip(j, Chip.GREEN)
        self.assertTrue(g.is_full())
