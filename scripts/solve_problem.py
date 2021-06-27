import sys
import tetris3d


def show(sol, opacity=1.0):
    points = tetris3d.brick.vol2pts(sol.volume)
    problem = []
    if len(points) > 0:
        problem.append(tetris3d.brick.Brick(points))
    tetris3d.display.Display.show(problem + sol.bricks, opacity=opacity)


def main():
    if len(sys.argv) not in [1, 2]:
        raise NotImplementedError(f'{sys.argv[0]} [id]')
    pid = 'card107' if len(sys.argv) in [1] else 'card' + sys.argv[1]
    problems = tetris3d.problems.ProblemsGenerator.generate(pid=pid)
    with_groups=[k for k in tetris3d.groups.VALID_GROUPS.keys()]
    # with_groups=['red', 'orange', 'green', 'blue']

    solutions = tetris3d.solver.Solver.solve(problems[0], with_groups)
    print(f'number of solutions {len(solutions)}')

    if len(solutions) > 0:
        print(solutions[0:8])
        show(solutions[0], opacity=1.0)
        ind = input('pause ')
        while True:
            try:
                ind = input('choose index of solutions to plot: ')
                show(solutions[int(ind)], opacity=1.0)
            except ValueError:
                pass


if __name__ == "__main__":
    main()
