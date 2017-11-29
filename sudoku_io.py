from sudoku_solver import *


def parse_sudoku(input_filename):
    # n: number of nodes in line/column
    # sep: separator between node values [spc: single space, tab: tab]
    # unknown_value: char used for marking unknown node value

    n = None
    myrange = None
    sep = None
    unknown_value = None

    parameter_mode = False
    sudoku_parsing_mode = False

    sudoku = None

    # The things get a bit uglier here.

    try:
        srow = 0  # sudoku row
        for line in open(input_filename, 'r'):

            if line[:2] == "?P":
                parameter_mode = True

            elif line[:2] == "?S":
                parameter_mode = False
                sudoku_parsing_mode = True

                if myrange is None:
                    myrange = [str(x) for x in range(0, n)]
                    sep = " "
                    unknown_value = "*"

                elif sep is None:
                    sep = " "
                    unknown_value = "*"

                elif unknown_value is None:
                    unknown_value = "*"

                sudoku = Sudoku(n, myrange)

            elif line[:2] == "?E":
                parameter_mode = False
                sudoku_parsing_mode = False

                return sudoku

            elif parameter_mode:
                data = line.split()

                if n is None:
                    n = int(data[0])

                elif myrange is None:
                    try:
                        ci = data.index("#")  # comment index
                        myrange = data[:ci]
                    except ValueError:
                        myrange = data

                elif sep is None:
                    if data[0] == "spc":
                        sep = " "
                    elif data[0] == "tab":
                        sep = "\t"
                    else:
                        sep = data[0]

                elif unknown_value is None:
                    if data[0] == "spc":
                        unknown_value = " "
                    elif data[0] == "tab":
                        unknown_value = "\t"
                    else:
                        unknown_value = data[0]

            elif sudoku_parsing_mode:
                values = line.split(sep=sep)

                for scol in range(0, n):
                    value = values[scol].strip()

                    if value in myrange:
                        sudoku.set_value(srow, scol, value)

                    elif value is unknown_value:
                        pass

                    else:
                        raise ValueError

                srow += 1

        return sudoku

    except ValueError:
        print("Invalid input file formatting.")

    except FaultySolution:
        print("Sudoku in input file is not valid.")


def write_solution_to_file(solutions, output_filename, sep=" "):

        with open(output_filename, "w") as file:

            if len(solutions) == 0:
                file.write("No solution was found.")

            elif len(solutions) == 1:

                solution = solutions[0]

                sol_keys = [x for (x, y) in list(solution.keys())]
                n = max(sol_keys) + 1

                for i in range(0, n):
                    line = ""

                    for j in range(0, n):
                        line += solution[(i, j)]
                        line += sep

                    line += "\n"
                    file.write(line)
                file.close()

            else:
                file.write("This feature is not implemented yet and apparently it works by itself, great.")