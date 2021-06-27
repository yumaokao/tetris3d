import tetris3d


def main():
    grouped_bricks = tetris3d.groups.GroupedBricksGenerator.generate()
    firebird = [
        grouped_bricks['blue'].replica(rotate=(0, 0, 1), offset=(0, 0, 1)),
        grouped_bricks['red'].replica(rotate=(0, 1, 3), offset=(1, 1, 1)),
        grouped_bricks['violet'].replica(rotate=(0, 2, 1), offset=(0, 2, 0)),
        grouped_bricks['green'].replica(rotate=(2, 0, 2), offset=(1, 2, 1)),
        grouped_bricks['indigo'].replica(rotate=(2, 1, 1), offset=(0, 3, 1)),
        grouped_bricks['yellow'].replica(rotate=(0, 2, 0), offset=(0, 2, 2)),
    ]
    swimbird = [
        grouped_bricks['blue'].replica(rotate=(0, 0, 1), offset=(1, 0, 0)),
        grouped_bricks['red'].replica(rotate=(2, 1, 3), offset=(3, 2, 0)),
        grouped_bricks['violet'].replica(rotate=(0, 2, 1), offset=(1, 2, 0)),
        grouped_bricks['green'].replica(rotate=(0, 0, 2), offset=(3, 1, 0)),
        grouped_bricks['indigo'].replica(rotate=(2, 1, 1), offset=(1, 3, 0)),
        grouped_bricks['yellow'].replica(rotate=(0, 2, 0), offset=(0, 2, 2)),
    ]
    tetris3d.display.Display.show(swimbird)


if __name__ == "__main__":
    main()
