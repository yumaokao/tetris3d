import tetris3d


def main():
    problems = tetris3d.problems.ProblemsGenerator.generate(pid='card106')
    tetris3d.display.Display.show(problems)


if __name__ == "__main__":
    main()
