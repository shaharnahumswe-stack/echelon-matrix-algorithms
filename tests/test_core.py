import numpy as np
import pytest

from echelon_matrix import determinant, inverse, matrix_rank, row_echelon_form


def test_rank_for_rectangular_matrix() -> None:
    matrix = np.array([[1, 2, 3], [2, 4, 6], [1, 1, 1]], dtype=float)
    assert matrix_rank(matrix) == 2


def test_determinant_matches_known_value() -> None:
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 10]], dtype=float)
    assert determinant(matrix) == pytest.approx(-3.0)


def test_inverse_matches_identity_product() -> None:
    matrix = np.array([[4, 7], [2, 6]], dtype=float)
    result = inverse(matrix)
    assert result is not None
    assert np.allclose(matrix @ result, np.eye(2))


def test_singular_matrix_has_no_inverse() -> None:
    matrix = np.array([[1, 2], [2, 4]], dtype=float)
    assert inverse(matrix) is None
    assert determinant(matrix) == pytest.approx(0.0)


def test_ref_has_zero_entries_below_pivots() -> None:
    matrix = np.array([[0, 2, 1], [1, 1, 0], [2, 3, 4]], dtype=float)
    ref, rank, swaps = row_echelon_form(matrix)
    assert rank == 3
    assert swaps >= 1
    assert np.allclose(np.tril(ref, k=-1), 0.0)


def test_non_square_determinant_rejected() -> None:
    with pytest.raises(ValueError):
        determinant([[1, 2, 3], [4, 5, 6]])
