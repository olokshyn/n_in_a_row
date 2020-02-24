from unittest import TestCase

import numpy as np

from n_in_a_row import grid, game
from n_in_a_row.win_state import WinState
from n_in_a_row.chip import Chip


class TestCheckWinInVector(TestCase):

    def test_too_small_vector(self):
        self.assertRaises(
            ValueError,
            game.check_win_in_vector,
            vec=np.zeros(3),
            chips_in_a_row=4
        )
        self.assertRaises(
            ValueError,
            game.check_win_in_vector,
            vec=np.zeros(2),
            chips_in_a_row=4
        )
        self.assertRaises(
            ValueError,
            game.check_win_in_vector,
            vec=np.zeros(1),
            chips_in_a_row=4
        )
        self.assertRaises(
            ValueError,
            game.check_win_in_vector,
            vec=np.zeros(0),
            chips_in_a_row=4
        )
        self.assertRaises(
            ValueError,
            game.check_win_in_vector,
            vec=np.zeros(6),
            chips_in_a_row=7
        )

    def test_empty_vector(self):
        self.assertEqual(
            WinState.DRAW,
            game.check_win_in_vector(np.zeros(4), 4)
        )
        self.assertEqual(
            WinState.DRAW,
            game.check_win_in_vector(np.zeros(6), 4)
        )
        self.assertEqual(
            WinState.DRAW,
            game.check_win_in_vector(np.zeros(6), 6)
        )

    def test_no_win(self):
        vec = np.array([1, 0, 1, 2, 1, 0, 2, 2, 2, 1, 1, 0, 1, 1, 2])
        self.assertEqual(WinState.DRAW, game.check_win_in_vector(vec, 4))

        vec = np.array([1, 1, 1, 2, 2, 2, 1, 0, 1, 0, 1])
        self.assertEqual(WinState.DRAW, game.check_win_in_vector(vec, 4))

        vec = np.array([2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 0, 2, 2, 2])
        self.assertEqual(WinState.DRAW, game.check_win_in_vector(vec, 6))

        vec = np.array([1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 0, 1])
        self.assertEqual(WinState.DRAW, game.check_win_in_vector(vec, 4))

        vec = np.array([0, 2, 2, 2, 2, 1, 1, 1, 1, 0])
        self.assertEqual(WinState.DRAW, game.check_win_in_vector(vec, 5))

    def test_win_only_green(self):
        vec = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(WinState.GREEN, game.check_win_in_vector(vec, 4))

        vec = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(WinState.GREEN, game.check_win_in_vector(vec, 7))

        vec = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(WinState.GREEN, game.check_win_in_vector(vec, 10))

    def test_win_only_red(self):
        vec = np.array([2, 2, 2, 2, 2])
        self.assertEqual(WinState.RED, game.check_win_in_vector(vec, 5))

        vec = np.array([0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2])
        self.assertEqual(WinState.RED, game.check_win_in_vector(vec, 5))

        vec = np.array([0, 0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 2, 0])
        self.assertEqual(WinState.RED, game.check_win_in_vector(vec, 5))

        vec = np.array([2, 2, 2])
        self.assertEqual(WinState.RED, game.check_win_in_vector(vec, 3))

    def test_win_at_the_beginning(self):
        vec = np.array([1, 1, 1, 1, 0, 2, 2, 1, 1, 1, 0, 1, 1])
        self.assertEqual(WinState.GREEN, game.check_win_in_vector(vec, 4))

        vec = np.array([2, 2, 2, 2, 1, 1, 1, 1, 0, 2, 1, 1])
        self.assertEqual(WinState.RED, game.check_win_in_vector(vec, 4))

        vec = np.array([1, 1, 1, 1, 1, 1, 1, 8, 9, 2, 2, 1, 1, 2, 2, 2, 2])
        self.assertEqual(WinState.GREEN, game.check_win_in_vector(vec, 7))

    def test_win_at_the_end(self):
        vec = np.array([1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2])
        self.assertEqual(WinState.RED, game.check_win_in_vector(vec, 5))

        vec = np.array([1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2])
        self.assertEqual(WinState.RED, game.check_win_in_vector(vec, 4))

        vec = np.array([0, 1, 1, 0, 2, 2, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(WinState.GREEN, game.check_win_in_vector(vec, 7))

    def test_win_in_the_middle(self):
        vec = np.array([2, 1, 0, 1, 0, 2, 2, 2, 2, 2, 1, 1, 1, 1, 0])
        self.assertEqual(WinState.RED, game.check_win_in_vector(vec, 5))

        vec = np.array([1, 1, 1, 0, 2, 2, 2, 2, 0, 1, 1, 1])
        self.assertEqual(WinState.RED, game.check_win_in_vector(vec, 4))

        vec = np.array([2, 2, 2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 0])
        self.assertEqual(WinState.GREEN, game.check_win_in_vector(vec, 6))


class TestCheckWinInDiagonal(TestCase):

    def test_no_win(self):
        mat = np.array([
            [1, 1, 1, 0, 1],
            [1, 2, 2, 1, 1],
            [1, 1, 1, 2, 2],
            [2, 2, 2, 1, 1]
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2]
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [1, 1, 1, 1, 1, 1],
            [2, 2, 1, 2, 2, 2],
            [1, 1, 1, 2, 2, 1],
            [2, 2, 2, 2, 2, 2]
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1]
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 0, 1, 0, 1, 1],
            [1, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 1, 0, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

    def test_win_in_main_diagonal(self):
        mat = np.array([
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
        ])
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
        ])
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
        ])
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat[::-1], 4))

    def test_win_in_sub_diagonal(self):
        mat = np.array([
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat[::-1], 4))

        mat = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
        ])
        self.assertEqual(WinState.DRAW, game.check_win_in_diagonal(mat, 4))
        self.assertEqual(WinState.GREEN, game.check_win_in_diagonal(mat[::-1], 4))


class TestGetWinState(TestCase):

    def test_win_in_row(self):
        g = grid.Grid(6, 7)

        g[5, 3] = Chip.GREEN
        g[5, 4] = Chip.RED
        g[5, 5] = Chip.GREEN
        g[5, 6] = Chip.GREEN

        g[4, 3] = Chip.RED
        g[4, 4] = Chip.RED
        g[4, 5] = Chip.RED
        g[4, 6] = Chip.RED

        self.assertEqual(WinState.RED, game.get_win_state(g, chips_in_a_row=4))

    def test_win_in_col(self):
        g = grid.Grid(6, 7)

        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(1, Chip.RED)

        self.assertEqual(WinState.RED, game.get_win_state(g, chips_in_a_row=4))

    def test_win_in_main_diagonal(self):
        g = grid.Grid(6, 7)

        g[5, 0] = Chip.RED
        g[4, 0] = Chip.RED
        g[3, 0] = Chip.RED
        g[2, 0] = Chip.GREEN

        g[5, 1] = Chip.RED
        g[4, 1] = Chip.RED
        g[3, 1] = Chip.GREEN

        g[5, 2] = Chip.RED
        g[4, 2] = Chip.GREEN

        g[5, 3] = Chip.GREEN

        self.assertEqual(WinState.GREEN, game.get_win_state(g, chips_in_a_row=4))

    def test_win_in_sub_diagonal(self):
        g = grid.Grid(6, 7)

        g[5, 0] = Chip.RED

        g[5, 1] = Chip.GREEN
        g[4, 1] = Chip.RED

        g[5, 2] = Chip.GREEN
        g[4, 2] = Chip.GREEN
        g[3, 2] = Chip.RED

        g[5, 3] = Chip.GREEN
        g[4, 3] = Chip.GREEN
        g[3, 3] = Chip.GREEN
        g[2, 3] = Chip.RED

        self.assertEqual(WinState.RED, game.get_win_state(g, chips_in_a_row=4))
