import random

import pytest
from scipy.optimize import linear_sum_assignment

from hungarian import (
    hungarian_algorithm,
    transpose,
    find_independent_zeros,
    find_covering_lines,
)


def assignment_cost(
    matrix: list[list[int]],
    assignment: list[tuple[int, int]]
) -> int:
    """Calculate the total cost of an assignment."""
    total = 0

    for row, col in assignment:
        total += matrix[row][col]

    return total


# Tests transposing a square matrix
def test_transpose_square():
    matrix = [
        [1, 2],
        [3, 4],
    ]
    expected = [
        [1, 3],
        [2, 4],
    ]
    assert transpose(matrix) == expected


# Tests transposing a rectangular matrix
def test_transpose_rectangular():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    expected = [
        [1, 4],
        [2, 5],
        [3, 6],
    ]
    assert transpose(matrix) == expected


# Tests transposing a matrix with one element
def test_transpose_single_element():
    assert transpose([[5]]) == [[5]]


# Tests finding independent zeros along the diagonal
def test_find_independent_zeros_diagonal():
    matrix = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]

    row_match, col_match = find_independent_zeros(matrix)
    assert row_match == [0, 1, 2]
    assert col_match == [0, 1, 2]


# Tests finding enough independent zeros for a complete assignment
def test_find_independent_zeros_complete_assignment():
    matrix = [
        [0, 5, 0],
        [0, 2, 5],
        [3, 0, 0],
    ]

    row_match, col_match = find_independent_zeros(matrix)
    assert -1 not in row_match
    assert -1 not in col_match
    for row, col in enumerate(row_match):
        assert matrix[row][col] == 0
    assert len(set(row_match)) == len(row_match)


# Tests when there are not enough independent zeros for an assignment
def test_find_independent_zeros_incomplete_assignment():
    matrix = [
        [0, 1, 1],
        [0, 2, 2],
        [3, 0, 4],
    ]

    row_match, col_match = find_independent_zeros(matrix)
    matches = sum(col != -1 for col in row_match)
    assert matches == 2


# Tests that the covering lines cover every zero
def test_covering_lines():
    matrix = [
        [0, 1, 1],
        [0, 2, 2],
        [3, 0, 4],
    ]

    row_match, col_match = find_independent_zeros(matrix)
    covered_rows, covered_cols = find_covering_lines(
        row_match,
        col_match,
        matrix,
    )

    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == 0:
                assert row in covered_rows or col in covered_cols


# Tests that the minimum number of covering lines is found
def test_covering_lines_minimum_number():
    matrix = [
        [0, 1, 1],
        [0, 2, 2],
        [3, 0, 4],
    ]

    row_match, col_match = find_independent_zeros(matrix)
    covered_rows, covered_cols = find_covering_lines(
        row_match,
        col_match,
        matrix,
    )

    assert len(covered_rows) + len(covered_cols) == 2


# Tests the Hungarian algorithm on a 2x2 matrix
def test_hungarian_simple():
    matrix = [
        [1, 10],
        [10, 1],
    ]

    assignment = hungarian_algorithm(matrix)
    assert set(assignment) == {(0, 0), (1, 1)}
    assert assignment_cost(matrix, assignment) == 2


# Tests the Hungarian algorithm on a larger example
def test_hungarian_example():
    matrix = [
        [6, 10, 5, 2],
        [3, 5, 7, 7],
        [9, 1, 8, 4],
        [10, 3, 12, 5],
    ]

    assignment = hungarian_algorithm(matrix)
    rows = [row for row, col in assignment]
    assert len(set(rows)) == len(matrix)
    cols = [col for row, col in assignment]
    assert len(set(cols)) == len(matrix)
    scipy_rows, scipy_cols = linear_sum_assignment(matrix)
    scipy_cost = sum(
        matrix[row][col]
        for row, col in zip(scipy_rows, scipy_cols)
    )
    assert assignment_cost(matrix, assignment) == scipy_cost


# Tests random matrices against SciPy's Hungarian algorithm
@pytest.mark.parametrize("seed", range(20))
def test_random_matrices_against_scipy(seed: int):
    random.seed(seed)
    n = random.randint(2, 8)
    matrix = [
        [random.randint(0, 100) for _ in range(n)]
        for _ in range(n)
    ]
    assignment = hungarian_algorithm(matrix)
    our_cost = assignment_cost(matrix, assignment)
    scipy_rows, scipy_cols = linear_sum_assignment(matrix)
    scipy_cost = sum(
        matrix[row][col]
        for row, col in zip(scipy_rows, scipy_cols)
    )
    assert our_cost == scipy_cost