import numpy as np
import typing
import typeguard
from .brick import Brick


# color in the box side
'''
VALID_GROUPS = {
    'red': [(0, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0)],  # green
    'orange': [(0, 1, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],  # orange
    'yellow': [(0, 0, 0), (0, 0, 1), (1, 0, 0)],  # yellow
    'green': [(0, 1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 1)],  # red
    'blue': [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 2, 1)],  # violet
    'indigo': [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 0, 1)],  # indigo
    'violet': [(0, 1, 1), (1, 0, 0), (1, 1, 0), (1, 1, 1)],  # blue
}
'''

# color in read bricks
VALID_GROUPS = {
    'red': [(0, 1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 1)],
    'orange': [(0, 1, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
    'green': [(0, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0)],
    'blue': [(0, 1, 1), (1, 0, 0), (1, 1, 0), (1, 1, 1)],
    'indigo': [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 0, 1)],
    'violet': [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 2, 1)],

    'yellow': [(0, 0, 0), (0, 0, 1), (1, 0, 0)],
}


@typeguard.typechecked
class GroupedBricksGenerator():
    @staticmethod
    def generate(
            groups: typing.List[str]=VALID_GROUPS.keys()) -> typing.Dict[str, Brick]:
        grouped_bricks = {
            g: Brick(np.array(VALID_GROUPS[g]), color=g) for g in groups}
        return grouped_bricks
