def hungarian_algorithm(cost_matrix: list[list[int]]) -> list[tuple[int, int]]:
    """
    Find the minimum-cost assignment using the Hungarian algorithm.

    Args:
        cost_matrix: Matrix containing the cost of each assignment.

    Returns:
        A list of (row, column) assignments.
    """
    # Make copy of cost matrix to modify
    copy = [row[:] for row in cost_matrix]

    # Row reduction
    for i, row in enumerate(copy):
        x = min(row)
        for j, val in enumerate(row):
            copy[i][j] = val - x

    # Column reduction
    t = transpose(copy)
    for i, row in enumerate(t):
        x = min(row)
        for j, val in enumerate(row):
            copy[j][i] = val - x

    # Keep trying until we find an assignment
    while True:
        row_match, col_match = find_independent_zeros(copy)

        covered_rows, covered_cols = find_covering_lines(
            row_match,
            col_match,
            copy
        )

        lines = len(covered_rows) + len(covered_cols)

        # Enough independent zeros -- we're done
        if lines == len(copy):
            return [(row, col) for row, col in enumerate(row_match)]

        # Find smallest uncovered value
        smallest: int | float = float("inf")

        for row in range(len(copy)):
            for col in range(len(copy[0])):
                if row not in covered_rows and col not in covered_cols:
                    smallest = min(smallest, copy[row][col])

        # Adjust the matrix
        for row in range(len(copy)):
            for col in range(len(copy[0])):

                # Covered twice
                if row in covered_rows and col in covered_cols:
                    copy[row][col] += smallest

                # Not covered
                elif row not in covered_rows and col not in covered_cols:
                    copy[row][col] -= smallest


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """
    Transpose a matrix.

    Args:
        matrix: Matrix to transpose.

    Returns:
        The transposed matrix.
    """
    transpose = [
        [0 for i in range(len(matrix))]
        for i in range(len(matrix[0]))
    ]

    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            transpose[j][i] = matrix[i][j]

    return transpose


def find_independent_zeros(
    matrix: list[list[int]]
) -> tuple[list[int], list[int]]:
    """
    Find zero entries that do not share rows or columns.

    Args:
        matrix: Reduced cost matrix.

    Returns:
        The column matched to each row and the row matched to each column.
    """
    n_rows = len(matrix)
    n_cols = len(matrix[0])

    # -1 means the row or column does not have a match
    row_match = [-1] * n_rows
    col_match = [-1] * n_cols

    def find_match(row: int, visited: set[int]) -> bool:
        """
        Try to find a zero column for a row.

        Args:
            row: Row to find a match for.
            visited: Columns already checked.

        Returns:
            True if a match was found, otherwise False.
        """
        for col in range(n_cols):
            if matrix[row][col] == 0 and col not in visited:
                visited.add(col)

                # Column is free, or its current row can move
                if col_match[col] == -1 or find_match(
                    col_match[col], visited
                ):
                    row_match[row] = col
                    col_match[col] = row
                    return True

        return False

    # Try to find a match for every row
    for row in range(n_rows):
        find_match(row, set())

    return row_match, col_match


def find_covering_lines(
    row_match: list[int],
    col_match: list[int],
    matrix: list[list[int]]
) -> tuple[set[int], set[int]]:
    """
    Find the rows and columns needed to cover all zeros.

    Args:
        row_match: Column matched to each row.
        col_match: Row matched to each column.
        matrix: Reduced cost matrix.

    Returns:
        Sets containing the covered rows and covered columns.
    """
    marked_rows: set[int] = set()
    marked_cols: set[int] = set()

    # Mark rows without an assigned zero
    for row in range(len(matrix)):
        if row_match[row] == -1:
            marked_rows.add(row)

    changed = True

    while changed:
        changed = False

        # Mark columns containing zeros in marked rows
        for row in list(marked_rows):
            for col in range(len(matrix[0])):
                if matrix[row][col] == 0 and col not in marked_cols:
                    marked_cols.add(col)
                    changed = True

        # Mark rows whose assigned zero is in a marked column
        for col in list(marked_cols):
            row = col_match[col]

            if row != -1 and row not in marked_rows:
                marked_rows.add(row)
                changed = True

    # Lines go through unmarked rows and marked columns
    covered_rows = set(range(len(matrix))) - marked_rows
    covered_cols = marked_cols

    return covered_rows, covered_cols


cost_matrix = [
    [6, 10, 5, 2],
    [3, 5, 7, 7],
    [9, 1, 8, 4],
    [10, 3, 12, 5]
]

print(hungarian_algorithm(cost_matrix))