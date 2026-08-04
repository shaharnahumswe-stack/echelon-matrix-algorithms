"""Core numerical algorithms for row-echelon operations.

The implementation intentionally avoids ``numpy.linalg`` so the elimination
steps remain explicit and easy to study.
"""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
import numpy.typing as npt

FloatMatrix = npt.NDArray[np.float64]
DEFAULT_EPS = 1e-12


def _as_float_matrix(matrix: npt.ArrayLike) -> FloatMatrix:
    """Return a defensive, two-dimensional float copy of ``matrix``."""
    array = np.asarray(matrix, dtype=np.float64)
    if array.ndim != 2:
        raise ValueError("matrix must be two-dimensional")
    if array.size == 0:
        raise ValueError("matrix must not be empty")
    return array.copy()


def row_echelon_form(
    matrix: npt.ArrayLike,
    *,
    eps: float = DEFAULT_EPS,
) -> Tuple[FloatMatrix, int, int]:
    """Convert a matrix to row-echelon form using partial pivoting.

    Returns:
        A tuple ``(ref, rank, swap_count)``.

    Notes:
        Partial pivoting improves numerical stability by selecting the largest
        available absolute pivot in each column.
    """
    if eps <= 0:
        raise ValueError("eps must be positive")

    ref = _as_float_matrix(matrix)
    row_count, column_count = ref.shape
    pivot_row = 0
    swap_count = 0

    for column in range(column_count):
        if pivot_row >= row_count:
            break

        relative_index = int(np.argmax(np.abs(ref[pivot_row:, column])))
        selected_row = pivot_row + relative_index
        pivot = ref[selected_row, column]

        if abs(pivot) <= eps:
            continue

        if selected_row != pivot_row:
            ref[[pivot_row, selected_row], :] = ref[[selected_row, pivot_row], :]
            swap_count += 1

        pivot = ref[pivot_row, column]
        if pivot_row + 1 < row_count:
            factors = ref[pivot_row + 1 :, column] / pivot
            ref[pivot_row + 1 :, column:] -= (
                factors[:, np.newaxis] * ref[pivot_row : pivot_row + 1, column:]
            )
            ref[pivot_row + 1 :, column] = 0.0

        pivot_row += 1

    ref[np.abs(ref) <= eps] = 0.0
    return ref, pivot_row, swap_count


def matrix_rank(matrix: npt.ArrayLike, *, eps: float = DEFAULT_EPS) -> int:
    """Compute matrix rank via Gaussian elimination."""
    _, rank, _ = row_echelon_form(matrix, eps=eps)
    return rank


def determinant(matrix: npt.ArrayLike, *, eps: float = DEFAULT_EPS) -> float:
    """Compute the determinant of a square matrix using elimination."""
    array = _as_float_matrix(matrix)
    rows, columns = array.shape
    if rows != columns:
        raise ValueError("determinant is defined here only for square matrices")

    ref, rank, swap_count = row_echelon_form(array, eps=eps)
    if rank < rows:
        return 0.0

    value = float(np.prod(np.diag(ref)))
    return -value if swap_count % 2 else value


def inverse(
    matrix: npt.ArrayLike,
    *,
    eps: float = DEFAULT_EPS,
) -> Optional[FloatMatrix]:
    """Compute a square matrix inverse using Gauss-Jordan elimination.

    Returns ``None`` when the matrix is singular.
    """
    if eps <= 0:
        raise ValueError("eps must be positive")

    array = _as_float_matrix(matrix)
    rows, columns = array.shape
    if rows != columns:
        raise ValueError("inverse is defined only for square matrices")

    augmented = np.hstack((array, np.eye(rows, dtype=np.float64)))

    for column in range(columns):
        relative_index = int(np.argmax(np.abs(augmented[column:, column])))
        selected_row = column + relative_index

        if abs(augmented[selected_row, column]) <= eps:
            return None

        if selected_row != column:
            augmented[[column, selected_row], :] = augmented[[selected_row, column], :]

        augmented[column, :] /= augmented[column, column]

        factors = augmented[:, column].copy()
        factors[column] = 0.0
        augmented -= factors[:, np.newaxis] * augmented[column : column + 1, :]

    result = augmented[:, columns:]
    result[np.abs(result) <= eps] = 0.0
    return result
