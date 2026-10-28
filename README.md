# Hungarian-Algorithm-from-Scratch
## Motivation
The hungarian algorithm is a optimization problem meant to solve assignment problems. An assignment problem is finding the optimal matching between 2 quantities minimizing a cost. Such as matching robots. to jobs that fit them minimizing the total amount of time robots spend working on tasks. This is normally a $O(n!)$ problem since it has to look though every permutation of robots doing tasks however the hungarian algorithm does it with $O(n^3)$ complexity.

## Use Cases
The Hungarian algorithm has many different applications such as in multi object tracking in videos -- matching objects detected in past frames to current ones based on distance or appearance similarity. It is also used in detection transformers to match predictions to ground truth. Additionally it can be used to assign people to classes or jobs or robots to jobs. 
## Explainer on how it works
The first step is called row and column reduction. The matrix is copied and in the copy the minimum is found for each row and subtracted from each element in the row. After this the minimum is found for each column and subtracted form each column. 

```python
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
```
The second step is finding the independent zeros which is finding all of the zeros that do not share a row or a column. It does this by using a recursive approach. find_match operates on a row and finds independent zeros there. It does this by looping over all the columns in the row and if it finds a zero then it checks if there are other zeros in the column and if no other zeros are there it assigns the column and row indices to the row_match and column_math lists.

```python
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
```
The third step is it finds the covering lines which is the minimum amount of lines that can cover all the zeros in the hungarian algorithm.

```python
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
```

The fourth step is to check if the number of found lines is equal to the total number of rows in the matrix. If it is this means that every element in the first list can be assigned to every element in the second list. Assignments are returned.

```python
lines = len(covered_rows) + len(covered_cols)

# Enough independent zeros -- we're done
if lines == len(copy):
    return [(row, col) for row, col in enumerate(row_match)]
```

The fifth step executes if the number of lines is not equal to the number of rows which means that not every assignment in list 1 has a clear assignment in list 2(That is 2 from list 1 might share a item from list 2). This just adjusts the matrix by finding the smallest uncovered value and adds it to cells that are covered twice and subtracts it from all uncovered cells. Then steps 2 - 5 are rerun until assignment is found.  

```python
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
```
## Discussion on when it works
This algorithm can only be applied to square matrices where it is possible to match each item from each of the 2 lists of quantities to each other. It cannot be used to match 1 item to 2 others for example. In addition to this it assumes the problem can be written in terms of a cost matrix and it cannot be easily than this algorithm will not help that much. However in square matrices where there is a optimal match between every item on the 2 lists it would work in all cases. 
