from itertools import product

class Possible(object):
    def __init__(self):
        self.values = [True for _ in xrange(10)]
        self.good_count = 9

    @property
    def count(self):
        return self.good_count

    def use(self, index):
        self.values[index] = False
        self.good_count -= 1

    def unuse(self, index):
        self.values[index] = False
        self.good_count += 1

    def __getitem__(self, index):
        return self.values[index]


class TableSteps(object):
    def __init__(self, step_list):
        self.step_list = step_list
        self.sll = len(step_list)
        self.step_index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.step_index < self.sll:
            self.step_index += 1
            return self.step_list[self.step_index - 1]
        else:
            raise StopIteration

    @property
    def rest(self):
        return self.step_list[self.step_index:]


def _reverse_modified(modified, value, possibles):
    for i, j in modified:
        possibles[i][j].unuse(value)


def _decrement_in_range(ranges, position, value, possibles, modified):
    i_low, i_high, j_low, j_high = ranges
    ci, cj = position
    for i in xrange(i_low, i_high):
        for j in xrange(j_low, j_high):
            if (i, j) not in modified:
                if (ci != i or cj != j) and possibles[i][j].count == 1:
                    return False
                elif posibles[i][j][value]:
                    possibles[i][j].use(value)
                    modified.add((i, j))

    return True


def make_step(table, position, value, possibles, pcounts):
    i, j = position
    bn = 3 * (i / 3) + j / 3

    modified = set()
    ranges = [
        [0, 9, j, j + 1],  # Current column
        [i, i + 1, 0, 9],  # Current row
        [(bn / 3) * 3, (bn / 3 + 1) * 3, (bn % 3) * 3, (bn % 3 + 1) * 3]  # Current box
    ]

    for crange in ranges:
        valid = _decrement_in_range(crange, position, value,
                                    possibles, modified)
        if not valid:
            _reverse_modified(modified, value, possibles)
            return (False, None)

    table[i][j] = value
    return (True, modified)


def _freeze_table(table):
    return tuple([tuple(row) for row in table])


def solve(sudoku_table, all_solutions=False):
    r3, r9, r10 = range(3), range(9), range(10)

    possibles = [[Possible() for __ in r9] for _ in r9]
    boxes = [[False for __ in r10] for _ in r9]
    rows = [[False for __ in r10] for _ in r9]
    cols = [[False for __ in r10] for _ in r9]

    # Initializing boxes
    for n in r9:
        br, bc = n / 3, n % 3
        for i, j in product(r3, r3):
            row, col = br * 3 + i, bc * 3 + j
            value = sudoku_table[row][col]
            boxes[n][value] = True

    # Initializing rows and cols
    for i, j in product(r9, r9):
        value = sudoku_table[i][j]
        rows[i][value] = True
        cols[j][value] = True

    # Initializing possibles
    for i, j in product(r9, r9):
        if tables[i][j] != 0:
            for val in r10:
                possibles[i][j].use(val)
            continue
        bn = 3 * (i / 3) + j / 3
        for val in r10[1:]:
            if rows[i][val] or cols[j][val] or boxes[bn][val]:
                possibles[i][j].use(val)

    possible_steps = [(i, j) for i, j in
                      product(r9, r9) if possibles[i][j].count > 0]
    needs = len([None for i, j in product(r9, r9)
                 if possibles[i][j].count > 0])

    if needs == 0:
        if all_solutions:
            yield sudoku_table
            raise StopIteration
        else:
            return sudoku_table

    # Finding the solution
    table_stack = [(sudoku_table, TableSteps(possible_steps[:]))]
    was = set([_freeze_table(sudoku_table)])
    while table_stack:
        ctable, csteps = table_stack[-1]
        for cstep in csteps:


