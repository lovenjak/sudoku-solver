import copy
import math


class FaultySolution(Exception):
    pass


class Sudoku:

    class Node:
        def __init__(self, sudoku, x, y):
            self.sudoku = sudoku
            self.x = x
            self.y = y
            self.value = None
            self.possible_values = copy.copy(sudoku.myrange)

            sqrt_n = round(math.sqrt(sudoku.n), 0)
            i = int(x / sqrt_n)
            j = int(y / sqrt_n)
            self.group_index = (i, j)

            sudoku.groups[(i, j)].append(self)

    def __init__(self, n, myrange):
        # n: number of rows/columns
        # range: list of possible node values

        self.n = n
        self.n_empty_nodes = n*n
        self.myrange = myrange

        # Create groups
        self.groups = dict()

        sqrt_n = int(round(math.sqrt(n), 0))

        for i in range(0, sqrt_n):
            for j in range(0, sqrt_n):
                self.groups[(i, j)] = []

        indices = list(range(0, n))
        self.xy_list = [(x, y) for x in indices for y in indices]

        nodes = dict()
        for (x, y) in self.xy_list:
            nodes[(x, y)] = self.Node(self, x, y)

        self.nodes = nodes

        self.sorted_candidates = [nodes[k] for k in nodes.keys()]
        self.sort_nodes()

    def sort_nodes(self):
        # Sort nodes by number of possible values. The nodes with smaller number of possible values should be tried
        # first, so an ordering is needed.

        candidates = copy.copy(self.sorted_candidates)
        candidates = [c for c in candidates if c.possible_values]

        self.sorted_candidates = sorted(candidates, key=lambda x: len(x.possible_values))

    def set_value(self, x, y, value):
        node = self.nodes[(x, y)]

        if value not in node.possible_values:
            raise FaultySolution

        node.value = value
        node.possible_values = []
        self.n_empty_nodes -= 1

        for new_x in range(0, self.n):
            if self.nodes[(new_x, y)].possible_values:
                self.remove_possibility(new_x, y, value)

        for new_y in range(0, self.n):
            if self.nodes[(x, new_y)].possible_values:
                self.remove_possibility(x, new_y, value)

        group_nodes = self.groups[node.group_index]

        for gn in group_nodes:
            if gn.possible_values and gn is not node:
                self.remove_possibility(gn.x, gn.y, value)

        self.sort_nodes()

        return self

    def remove_possibility(self, x, y, value):
        node = self.nodes[(x, y)]
        if value in node.possible_values:
            node.possible_values.remove(value)

        if len(node.possible_values) == 0:
            raise FaultySolution

        if len(node.possible_values) == 1:
            self.set_value(x, y, node.possible_values[0])


class SudokuSolver:

    def __init__(self):
        pass

    def __call__(self, sudoku, solutions):

        if sudoku.n_empty_nodes == 0:  # Apparently there is a solution.
            print("Found a solution.")

            solution = dict()
            for i in range(0, sudoku.n):
                for j in range(0, sudoku.n):
                    solution[(i, j)] = sudoku.nodes[(i, j)].value

            solutions.append(solution)

        else:
            # Get top candidate and try all possible values in generator.
            tc = sudoku.sorted_candidates[0]
            solution_generator = (sudoku.set_value(tc.x, tc.y, pv) for pv in tc.possible_values)

            try:
                for possible_solution in solution_generator:
                        self.__call__(possible_solution, solutions)

            except FaultySolution:
                pass
