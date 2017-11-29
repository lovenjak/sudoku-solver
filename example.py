import sudoku_io as sio
import sudoku_solver as ss


def main():

    sudoku = sio.parse_sudoku("mesi.sud")

    solutions = []

    solver = ss.SudokuSolver()
    solver(sudoku, solutions)

    sio.write_solution_to_file(solutions, "mesi-solution.txt")


if __name__ == "__main__":
    main()