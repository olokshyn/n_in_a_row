import unittest

from copy import deepcopy

from n_in_a_row.chip import Chip
from n_in_a_row.win_state import WinState
from n_in_a_row.grid import Grid
from n_in_a_row.game_state.game_state import GameState
from n_in_a_row.game_state.game_tree_builder import GameTreeBuilder


class TestGameTreeBuilder(unittest.TestCase):

    def test_two_by_two(self):
        tree_builder = GameTreeBuilder(
            GameState(
                Grid(rows=2, cols=2),
                next_chip=Chip.GREEN,
                chips_in_a_row=2
            )
        )
        tree_builder.build_solution_tree()

        # root
        # 0 0
        # 0 0
        g = Grid(rows=2, cols=2)
        gs = GameState(g, Chip.GREEN, chips_in_a_row=2)
        node = tree_builder.root
        self.assertEqual(gs, node)
        self.assertIsNone(node.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 6
            },
            node.win_states_counter
        )
        self.assertListEqual(
            [],
            node.parents
        )

        # root -> 0
        # 0 0
        # 1 0
        g0 = deepcopy(g)
        g0.drop_chip(0, Chip.GREEN)
        gs0 = GameState(g0, Chip.RED, chips_in_a_row=2)
        node0 = tree_builder.root.children[0]
        self.assertEqual(gs0, node0)
        self.assertIsNone(node0.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 3
            },
            node0.win_states_counter
        )
        self.assertListEqual(
            [gs],
            node0.parents
        )

        # root -> 0 -> 0
        # 2 0
        # 1 0
        g00 = deepcopy(g0)
        g00.drop_chip(0, Chip.RED)
        gs00 = GameState(g00, Chip.GREEN, chips_in_a_row=2)
        node00 = tree_builder.root.children[0].children[0]
        self.assertEqual(gs00, node00)
        self.assertIsNone(node00.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 1
            },
            node00.win_states_counter
        )
        self.assertListEqual(
            [gs0],
            node00.parents
        )

        # root -> 0 -> 0 -> 0
        # 2 0
        # 1 1
        # win: 1
        g000 = deepcopy(g00)
        g000.drop_chip(1, Chip.GREEN)
        gs000 = GameState(g000, Chip.RED, chips_in_a_row=2)
        node000 = tree_builder.root.children[0].children[0].children[0]
        self.assertEqual(gs000, node000)
        self.assertEqual(node000.win_state, WinState.GREEN)
        self.assertEqual(
            {
                WinState.GREEN: 1
            },
            node000.win_states_counter
        )
        self.assertListEqual(
            [gs00],
            node000.parents
        )

        # root -> 0 -> 1
        # 0 0
        # 1 2
        g01 = deepcopy(g0)
        g01.drop_chip(1, Chip.RED)
        gs01 = GameState(g01, Chip.GREEN, chips_in_a_row=2)
        node01 = tree_builder.root.children[0].children[1]
        self.assertEqual(gs01, node01)
        self.assertIsNone(node01.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 2
            },
            node01.win_states_counter
        )
        self.assertListEqual(
            [gs0],
            node01.parents
        )

        # root -> 0 -> 1 -> 0
        # 1 0
        # 1 2
        # win: 1
        g010 = deepcopy(g01)
        g010.drop_chip(0, Chip.GREEN)
        gs010 = GameState(g010, Chip.RED, chips_in_a_row=2)
        node010 = tree_builder.root.children[0].children[1].children[0]
        self.assertEqual(gs010, node010)
        self.assertEqual(WinState.GREEN, node010.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 1
            },
            node010.win_states_counter
        )
        self.assertListEqual(
            [gs01],
            node010.parents
        )

        # root -> 0 -> 1 -> 1
        # 0 1
        # 1 2
        # win: 1
        g011 = deepcopy(g01)
        g011.drop_chip(1, Chip.GREEN)
        gs011 = GameState(g011, next_chip=Chip.RED, chips_in_a_row=2)
        node011 = tree_builder.root.children[0].children[1].children[1]
        self.assertEqual(gs011, node011)
        self.assertEqual(WinState.GREEN, node011.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 1
            },
            node011.win_states_counter
        )
        self.assertListEqual(
            [gs01],
            node011.parents
        )

        # root -> 1
        # 0 0
        # 0 1
        g1 = deepcopy(g)
        g1.drop_chip(1, Chip.GREEN)
        gs1 = GameState(g1, Chip.RED, chips_in_a_row=2)
        node1 = tree_builder.root.children[1]
        self.assertEqual(gs1, node1)
        self.assertIsNone(node1.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 3
            },
            node1.win_states_counter
        )
        self.assertListEqual(
            [gs],
            node1.parents
        )

        # root -> 1 -> 0
        # 0 0
        # 2 1
        g10 = deepcopy(g1)
        g10.drop_chip(0, Chip.RED)
        gs10 = GameState(g10, Chip.GREEN, chips_in_a_row=2)
        node10 = tree_builder.root.children[1].children[0]
        self.assertEqual(gs10, node10)
        self.assertIsNone(node10.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 2
            },
            node10.win_states_counter
        )
        self.assertListEqual(
            [gs1],
            node10.parents
        )

        # root -> 1 -> 0 -> 0
        # 1 0
        # 2 1
        # win: 1
        g100 = deepcopy(g10)
        g100.drop_chip(0, Chip.GREEN)
        gs100 = GameState(g100, Chip.RED, chips_in_a_row=2)
        node100 = tree_builder.root.children[1].children[0].children[0]
        self.assertEqual(gs100, node100)
        self.assertEqual(WinState.GREEN, node100.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 1
            },
            node100.win_states_counter
        )
        self.assertListEqual(
            [gs10],
            node100.parents
        )

        # root -> 1 -> 0 -> 1
        # 0 1
        # 2 1
        # win: 1
        g101 = deepcopy(g10)
        g101.drop_chip(1, Chip.GREEN)
        gs101 = GameState(g101, Chip.RED, chips_in_a_row=2)
        node101 = tree_builder.root.children[1].children[0].children[1]
        self.assertEqual(gs101, node101)
        self.assertEqual(WinState.GREEN, node101.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 1
            },
            node101.win_states_counter
        )
        self.assertListEqual(
            [gs10],
            node101.parents
        )

        # root -> 1 -> 1
        # 0 2
        # 0 1
        g11 = deepcopy(g1)
        g11.drop_chip(1, Chip.RED)
        gs11 = GameState(g11, Chip.GREEN, chips_in_a_row=2)
        node11 = tree_builder.root.children[1].children[1]
        self.assertEqual(gs11, node11)
        self.assertIsNone(node11.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 1
            },
            node11.win_states_counter
        )
        self.assertListEqual(
            [gs1],
            node11.parents
        )

        # root -> 1 -> 1 -> 0
        # 0 2
        # 1 1
        # win: 1
        g110 = deepcopy(g11)
        g110.drop_chip(0, Chip.GREEN)
        gs110 = GameState(g110, Chip.RED, chips_in_a_row=2)
        node110 = tree_builder.root.children[1].children[1].children[0]
        self.assertEqual(gs110, node110)
        self.assertEqual(WinState.GREEN, node110.win_state)
        self.assertEqual(
            {
                WinState.GREEN: 1
            },
            node110.win_states_counter
        )
        self.assertListEqual(
            [gs11],
            node110.parents
        )

        # Check child references

        # root
        # 0 0
        # 0 0
        self.assertListEqual(
            [gs0, gs1],
            node.children
        )
        self.assertSetEqual(
            {gs000.game_state_id, gs010.game_state_id, gs011.game_state_id,
             gs100.game_state_id, gs101.game_state_id, gs110.game_state_id},
            node.child_leaf_node_ids
        )

        # root -> 0
        # 0 0
        # 1 0
        self.assertListEqual(
            [gs00, gs01],
            node0.children
        )
        self.assertSetEqual(
            {gs000.game_state_id, gs010.game_state_id, gs011.game_state_id},
            node0.child_leaf_node_ids
        )

        # root -> 0 -> 0
        # 2 0
        # 1 0
        self.assertListEqual(
            [gs000],
            node00.children
        )
        self.assertSetEqual(
            {gs000.game_state_id},
            node00.child_leaf_node_ids
        )

        # root -> 0 -> 0 -> 0
        # 2 0
        # 1 1
        # win: 1
        self.assertListEqual(
            [],
            node000.children
        )
        self.assertSetEqual(
            {gs000.game_state_id},
            node000.child_leaf_node_ids
        )

        # root -> 0 -> 1
        # 0 0
        # 1 2
        self.assertListEqual(
            [gs010, gs011],
            node01.children
        )
        self.assertSetEqual(
            {gs010.game_state_id, gs011.game_state_id},
            node01.child_leaf_node_ids
        )

        # root -> 0 -> 1 -> 0
        # 1 0
        # 1 2
        # win: 1
        self.assertListEqual(
            [],
            node010.children
        )
        self.assertSetEqual(
            {gs010.game_state_id},
            node010.child_leaf_node_ids
        )

        # root -> 0 -> 1 -> 1
        # 0 1
        # 1 2
        # win: 1
        self.assertListEqual(
            [],
            node011.children
        )
        self.assertSetEqual(
            {gs011.game_state_id},
            node011.child_leaf_node_ids
        )

        # root -> 1
        # 0 0
        # 0 1
        self.assertListEqual(
            [gs10, gs11],
            node1.children
        )
        self.assertSetEqual(
            {gs100.game_state_id, gs101.game_state_id, gs110.game_state_id},
            node1.child_leaf_node_ids
        )

        # root -> 1 -> 0
        # 0 0
        # 2 1
        self.assertListEqual(
            [gs100, gs101],
            node10.children
        )
        self.assertSetEqual(
            {gs100.game_state_id, gs101.game_state_id},
            node10.child_leaf_node_ids
        )

        # root -> 1 -> 0 -> 0
        # 1 0
        # 2 1
        # win: 1
        self.assertListEqual(
            [],
            node100.children
        )
        self.assertSetEqual(
            {gs100.game_state_id},
            node100.child_leaf_node_ids
        )

        # root -> 1 -> 0 -> 1
        # 0 1
        # 2 1
        # win: 1
        self.assertListEqual(
            [],
            node101.children
        )
        self.assertSetEqual(
            {gs101.game_state_id},
            node101.child_leaf_node_ids
        )

        # root -> 1 -> 1
        # 0 2
        # 0 1
        self.assertListEqual(
            [gs110],
            node11.children
        )
        self.assertSetEqual(
            {gs110.game_state_id},
            node11.child_leaf_node_ids
        )

        # root -> 1 -> 1 -> 0
        # 0 2
        # 1 1
        # win: 1
        self.assertListEqual(
            [],
            node110.children
        )
        self.assertSetEqual(
            {gs110.game_state_id},
            node110.child_leaf_node_ids
        )


if __name__ == '__main__':
    unittest.main()
