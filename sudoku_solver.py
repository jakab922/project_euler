def _reverse_modified(modified, value, possibles, pcounts):
    for i, j in modified:
        possibles[i][j][value] = True
        pcounts[i][j] += 1


def _decrement_in_range(ranges, position, value, possibles, pcounts, modified):
    i_low, i_high, j_low, j_high = ranges
    ci, cj = position
    for i in xrange(i_low, i_high):
        for j in xrange(j_low, j_high):
            if (i, j) not in modified:
                if (ci != i or cj != j) and pcounts[i][j] == 1:
                    return False
                else:
                    pcounts[i][j] -= 1
                    possibles[i][j][value] = False
                    modified.add((i, j))

    return True


def make_step(table, position, value, possibles, pcounts):
    i, j = position
    if not possibles[x][y][value]:  # Probably we should check against this outside
        return False
    row_needs, col_needs, box_needs = needs
    bn = 3 * (i / 3) + j / 3

    modified = set()
    ranges = [
        [0, 9, j, j + 1],  # Current column
        [i, i + 1, 0, 9],  # Current row
        [(bn / 3) * 3, (bn / 3 + 1) * 3, (bn % 3) * 3, (bn % 3 + 1) * 3]  # Current box
    ]

    for crange in ranges:
        valid = _decrement_in_range(crange, position, value, possibles,
                                    pcounts, modified)
        if not valid:
            _reverse_modified(modified, value, possibles, pcounts)
            return (False, None)

    table[i][j] = value
    return (True, modified)


def reverse_step(table, position, value, possibles, pcounts, modified):
    ci, cj = position
    for i, j in modified:
        possibles[i][j][value] = True
        pcounts[i][j] += 1

    table[ci][cj] = 0


def solve(sudoku_table, all_solutions=False):
    pcounts = [[9 for __ in xrange(9)] for _ in xrange(9)]
    possibles = [[[True for _ in xrange(9)] for _j in xrange(9)]
                 for _i in xrange(9)]
    possible_steps = set()

    boxes = [[False for __ in xrange(10)] for _ in xrange(9)]
    rows = [[False for __ in xrange(10)] for _ in xrange(9)]
    cols = [[False for __ in xrange(10)] for _ in xrange(9)]

    was = set()

    # Initializing boxes
    for n in xrange(9):
        br = n / 3
        bc = n % 3
        for i in xrange(3):
            for j in xrange(3):
                row = br * 3 + i
                col = bc * 3 + j
                value = sudoku_table[row][col]
                boxes[n][value] = True

    # Initializing rows and cols
    for i in xrange(9):
        for j in xrange(9):
            value = sudoku_table[i][j]
            rows[i][j] = True
            cols[j][i] = True

    # Initializing possibles
    for i in xrange(9):
        for j in xrange(9):
            if tables[i][j] != 0:
                for val in xrange(9):
                    possibles[i][j][val] = False
            continue
            bn = 3 * (i / 3) + j / 3
            for val in xrange(1, 9):
                if rows[i][val] or cols[j][val] or boxes[bn][val]:
                    possibles[i][j][val] = False

    for i in xrange(9):
        for j in xrange(9):
            pcounts[i][j] = sum(map(lambda x: 1 if x else 0,
                                    possibles[i][j][1:]))
            if pcounts[i][j] != 0:
                possible_steps.add((i, j))

    # Finding the solution

    while state_stack:
        current_state = state_stack.pop()
        for place in places:
            for value in xrange(1, 9):

