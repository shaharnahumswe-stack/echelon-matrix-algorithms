"""Linear-algebra algorithms based on Gaussian and Gauss-Jordan elimination."""

from .core import determinant, inverse, matrix_rank, row_echelon_form

__all__ = ["determinant", "inverse", "matrix_rank", "row_echelon_form"]
