import tetris3d
import cProfile
import tracemalloc


def show(sol, opacity=1.0):
    points = tetris3d.brick.vol2pts(sol.volume)
    tetris3d.display.Display.show(
        [tetris3d.brick.Brick(points)] + sol.bricks, opacity=opacity)


def main():
    problems = tetris3d.problems.ProblemsGenerator.generate(pid='card103')
    tracemalloc.start(25)
    with cProfile.Profile() as pr:
        solutions = tetris3d.solver.Solver.solve(
            problems[0], ['red', 'orange', 'green'])

    print('cProfile status')
    pr.print_stats(sort=True)

    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics('traceback')
    for i in range(4):
        print(f'memory blocks[{i}]')
        stat = snapshot.statistics('traceback')[i]
        print(f'{stat.count} memory blocks: {stat.size / 1024 / 1024} MiB')
        for line in stat.traceback.format():
            print(line)

    print(f'number of solutions {len(solutions)}')
    show(solutions[0], opacity=1.0)


if __name__ == "__main__":
    main()
