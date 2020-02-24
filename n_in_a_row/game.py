import numpy as np

from n_in_a_row.grid import Grid
from n_in_a_row.win_state import WinState


def check_win_in_vector(vec: np.array, chips_in_a_row: int) -> WinState:
    if len(vec) < chips_in_a_row:
        raise ValueError('Vector is too small')
    for shift in range(0, len(vec) - chips_in_a_row + 1):
        check_vec = vec[shift:shift + chips_in_a_row]
        for win_state in [WinState.GREEN, WinState.RED]:
            if np.all(check_vec == win_state.value):
                return win_state
    return WinState.DRAW


def check_win_in_diagonal(matrix: np.array, chips_in_a_row: int) -> WinState:
    offset_range = range(
        -(matrix.shape[0] - chips_in_a_row),
        (matrix.shape[1] - chips_in_a_row) + 1
    )
    for offset in offset_range:
        diag = matrix.diagonal(offset=offset)
        win_state = check_win_in_vector(diag, chips_in_a_row)
        if win_state != WinState.DRAW:
            return win_state
    return WinState.DRAW


def check_win_in_row(grid: Grid, chips_in_a_row: int) -> WinState:
    for grid_row in grid:
        win_state = check_win_in_vector(grid_row, chips_in_a_row)
        if win_state != WinState.DRAW:
            return win_state
    return WinState.DRAW


def check_win_in_column(grid: Grid, chips_in_a_row: int) -> WinState:
    for grid_col in grid.T:
        win_state = check_win_in_vector(grid_col, chips_in_a_row)
        if win_state != WinState.DRAW:
            return win_state
    return WinState.DRAW


def check_win_in_main_diag(grid: Grid, chips_in_a_row: int) -> WinState:
    return check_win_in_diagonal(grid, chips_in_a_row)


def check_win_in_sub_diag(grid: Grid, chips_in_a_row: int) -> WinState:
    return check_win_in_diagonal(grid.grid[::-1], chips_in_a_row)


def get_win_state(grid: Grid, chips_in_a_row: int) -> WinState:
    checks = {
        'row': check_win_in_row,
        'col': check_win_in_column,
        'main diag': check_win_in_main_diag,
        'sub diag': check_win_in_sub_diag
    }
    for check_name, check in checks.items():
        win_state = check(grid, chips_in_a_row)
        if win_state != WinState.DRAW:
            return win_state

    if grid.is_full():
        return WinState.DRAW

    raise GameNotFinishedError()


class GameError(Exception):
    pass


class GameNotFinishedError(GameError):
    pass


class GameFinishedError(GameError):
    pass
