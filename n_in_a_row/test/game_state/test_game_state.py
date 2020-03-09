import unittest
from copy import deepcopy

import numpy as np

from n_in_a_row.grid import Grid, GridIndex, CellError
from n_in_a_row.chip import Chip
from n_in_a_row.win_state import WinState
from n_in_a_row.game_state.game_state import GameState, GameFinishedError


class TestInit(unittest.TestCase):

    def test_win_state(self):
        g = Grid(rows=3, cols=4)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.RED)

        gs = GameState(g, next_chip=Chip.RED, chips_in_a_row=4)
        self.assertIsNone(gs.win_state)

        g = Grid(rows=3, cols=4)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.GREEN)

        gs = GameState(g, next_chip=Chip.RED, chips_in_a_row=4)
        self.assertEqual(WinState.GREEN, gs.win_state)

        g = Grid(rows=1, cols=4)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.GREEN)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.RED)

        gs = GameState(g, next_chip=Chip.RED, chips_in_a_row=4)
        self.assertEqual(WinState.DRAW, gs.win_state)

    def test_copy(self):
        g = Grid(rows=1, cols=4)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.GREEN)

        gs = GameState(g, next_chip=Chip.RED, chips_in_a_row=4, copy_grid=True)
        g.drop_chip(2, Chip.GREEN)
        self.assertEqual(Chip.GREEN, g[0, 2])
        self.assertEqual(Chip.EMPTY, gs.grid[0, 2])

        gs = GameState(g, next_chip=Chip.RED, chips_in_a_row=4, copy_grid=False)
        g.drop_chip(3, Chip.GREEN)
        self.assertEqual(Chip.GREEN, g[0, 3])
        self.assertEqual(Chip.GREEN, gs.grid[0, 3])


class TestGameStateId(unittest.TestCase):

    @staticmethod
    def _create_same_grids():
        g1 = Grid(rows=3, cols=3)
        g1.drop_chip(0, Chip.GREEN)
        g1.drop_chip(1, Chip.RED)
        g1.drop_chip(2, Chip.GREEN)
        g2 = Grid(rows=3, cols=3)
        g2.drop_chip(2, Chip.GREEN)
        g2.drop_chip(1, Chip.RED)
        g2.drop_chip(0, Chip.GREEN)
        return g1, g2

    def test_same(self):
        g1, g2 = self._create_same_grids()
        gs1 = GameState(g1, next_chip=Chip.GREEN, chips_in_a_row=4)
        gs2 = GameState(g2, next_chip=Chip.GREEN, chips_in_a_row=4)
        self.assertEqual(gs1.game_state_id, gs2.game_state_id)

    def test_diff_grid(self):
        g1 = Grid(rows=3, cols=3)
        g1.drop_chip(0, Chip.GREEN)
        g1.drop_chip(1, Chip.RED)
        g1.drop_chip(2, Chip.GREEN)
        g2 = Grid(rows=3, cols=3)
        g2.drop_chip(2, Chip.RED)
        g2.drop_chip(1, Chip.GREEN)
        g2.drop_chip(0, Chip.RED)

        gs1 = GameState(g1, next_chip=Chip.GREEN, chips_in_a_row=4)
        gs2 = GameState(g2, next_chip=Chip.GREEN, chips_in_a_row=4)
        self.assertNotEqual(gs1.game_state_id, gs2.game_state_id)

    def test_same_grid_diff_next_chip(self):
        g1, g2 = self._create_same_grids()
        gs1 = GameState(g1, next_chip=Chip.GREEN, chips_in_a_row=4)
        gs2 = GameState(g2, next_chip=Chip.RED, chips_in_a_row=4)
        self.assertNotEqual(gs1.game_state_id, gs2.game_state_id)

    def test_same_grid_diff_chips_in_a_row(self):
        g1, g2 = self._create_same_grids()
        gs1 = GameState(g1, next_chip=Chip.RED, chips_in_a_row=3)
        gs2 = GameState(g2, next_chip=Chip.RED, chips_in_a_row=4)
        self.assertNotEqual(gs1.game_state_id, gs2.game_state_id)


class TestMakeMove(unittest.TestCase):

    def test_ok(self):
        g = Grid(rows=3, cols=3)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(2, Chip.GREEN)

        index = GridIndex(1, 0)
        next_g = deepcopy(g)
        next_g[index] = Chip.GREEN

        gs = GameState(g, next_chip=Chip.GREEN, chips_in_a_row=4)
        child = gs.make_move(index)

        self.assertTrue(np.all(next_g.grid == child.grid.grid))
        self.assertEqual(Chip.EMPTY, gs.grid[index])
        self.assertEqual(Chip.RED, child.next_chip)
        self.assertEqual(4, child.chips_in_a_row)
        self.assertIsNone(child.win_state)
        self.assertIsNone(child.win_states_counter)
        self.assertIn(gs, child.parents)
        self.assertIn(child, gs.children)
        self.assertEqual(0, len(gs.child_leaf_node_ids))

        gs.grid[1, 1] = Chip.GREEN
        self.assertEqual(Chip.EMPTY, child.grid[1, 1])

    def test_no_move_win(self):
        g = Grid(rows=2, cols=4)
        g.drop_chip(0, Chip.RED)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(2, Chip.RED)
        g.drop_chip(3, Chip.RED)

        gs = GameState(g, next_chip=Chip.GREEN, chips_in_a_row=4)

        self.assertRaises(GameFinishedError, lambda: gs.make_move(GridIndex(0, 0)))
        self.assertRaises(GameFinishedError, lambda: gs.make_move(GridIndex(0, 1)))
        self.assertRaises(GameFinishedError, lambda: gs.make_move(GridIndex(0, 2)))
        self.assertRaises(GameFinishedError, lambda: gs.make_move(GridIndex(0, 3)))

    def test_no_move_draw(self):
        g = Grid(rows=1, cols=4)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.RED)
        g.drop_chip(2, Chip.GREEN)
        g.drop_chip(3, Chip.RED)

        gs = GameState(g, next_chip=Chip.RED, chips_in_a_row=4)

        self.assertRaises(GameFinishedError, lambda: gs.make_move(GridIndex(0, 0)))
        self.assertRaises(GameFinishedError, lambda: gs.make_move(GridIndex(0, 1)))
        self.assertRaises(GameFinishedError, lambda: gs.make_move(GridIndex(0, 2)))
        self.assertRaises(GameFinishedError, lambda: gs.make_move(GridIndex(0, 3)))

    def test_invalid_move(self):
        g = Grid(rows=2, cols=4)
        g.drop_chip(0, Chip.GREEN)
        g.drop_chip(1, Chip.RED)

        gs = GameState(g, next_chip=Chip.RED, chips_in_a_row=4)

        self.assertRaises(CellError, lambda: gs.make_move(GridIndex(1, 0)))
        self.assertRaises(CellError, lambda: gs.make_move(GridIndex(0, 2)))


if __name__ == '__main__':
    unittest.main()
