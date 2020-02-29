from n_in_a_row.chip import Chip
from n_in_a_row.grid import Grid
from n_in_a_row.game_state import GameState
from game_state import GameTreeBuilder


if __name__ == '__main__':
    tree_builder = GameTreeBuilder(
        GameState(
            Grid(rows=3, cols=3),
            next_chip=Chip.GREEN,
            chips_in_a_row=3
        )
    )

    from time import time

    start = time()
    tree_builder.build_solution_tree()
    end = time()

    print(f'Took {end - start} secs')

    print(tree_builder)
