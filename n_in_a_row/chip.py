import enum


class Chip(enum.Enum):

    EMPTY = 0
    GREEN = 1
    RED = 2


def swap_chip(chip: Chip) -> Chip:
    if chip == Chip.EMPTY:
        raise ValueError('Cannot swap empty chip!')
    if chip == Chip.GREEN:
        return chip.RED
    if chip == Chip.RED:
        return chip.GREEN
    raise RuntimeError('Only two chips are supported')
