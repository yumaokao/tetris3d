import typing
import dataclasses
import itertools
import functools
import multiprocessing
import numpy as np
import tqdm
import scipy.ndimage
from . import brick
from . import groups
from . import problems


@dataclasses.dataclass
class Solution:
    volume: np.ndarray
    bricks: typing.List['Brick']


class Solver():
    @staticmethod
    def fit(sol, volbricks, stack_vol, kernel) -> typing.List[Solution]:
        possible_solutions = []
        delta_vol = sol.volume - stack_vol
        left_mask = delta_vol.min(axis=(1, 2, 3)) >= 0
        for vb in itertools.compress(volbricks, left_mask):
            left_vol = sol.volume - vb.volume
            convs = scipy.ndimage.convolve(
                left_vol, kernel, mode='constant', cval=0)

            # refactored version with np.logical_and
            if np.count_nonzero(np.logical_and(left_vol > 0, convs == 0)) > 0:
                continue
            possible_solutions.append(Solution(
                sol.volume - vb.volume, sol.bricks + [vb.brick]))

            # orignal version with for loop
            '''
            is_possible = True
            for p in brick.vol2pts(left_vol):
                if convs[p[0], p[1], p[2]] in [0]:
                    is_possible = False
                    break
            if is_possible:
                possible_solutions.append(Solution(
                    sol.volume - vb.volume, sol.bricks + [vb.brick]))
            '''
        return possible_solutions

    @staticmethod
    def solve(problem, with_groups) -> typing.List[Solution]:
        ''' with_groups: ['red', ...]
            returns: solutions
        '''
        grouped_bricks = groups.GroupedBricksGenerator.generate(with_groups)
        counts = 0
        for color, gbrick in grouped_bricks.items():
            counts += gbrick.count
        if problem.count < counts:
            raise ValueError('problem points small than all groups counts')

        kernel = k = np.array([
                [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
                [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
            ], dtype=np.int8)

        grouped_volume_bricks = {
            k: gb.possible(problem.volume()) for k,gb in grouped_bricks.items()}
        for g, gv in grouped_volume_bricks.items():
            print(f'{g}: {len(gv)}')

        solutions = [Solution(problem.volume(), [])]
        for group in with_groups:
            print(f'number of solutions {len(solutions)} to group {group}')
            new_solutions = []
            volbricks = grouped_volume_bricks[group]
            stack_vol = np.stack([v.volume for v in volbricks])

            # Solver.fit, serial version
            fit_func = functools.partial(
                Solver.fit,
                volbricks=volbricks, stack_vol=stack_vol, kernel=kernel)
            '''
            for sol in tqdm.tqdm(solutions):
                new_solutions.append(fit_func(sol))
            '''
            with tqdm.tqdm(total=len(solutions)) as pbar:
                while len(solutions) > 0:
                    sol = solutions.pop()
                    new_solutions.append(fit_func(sol))
                    pbar.update()

            # Solver.fit, multiprocessing version
            '''
            fit_func = functools.partial(
                Solver.fit,
                volbricks=volbricks, stack_vol=stack_vol, kernel=kernel)
            with multiprocessing.Pool() as pool:
                with tqdm.tqdm(total=len(solutions)) as pbar:
                    for r in pool.imap_unordered(fit_func, solutions, 128):
                        pbar.update()
                        new_solutions.append(r)
            '''
            solutions = list(itertools.chain(*new_solutions))
        return solutions
