# Project summary

This academic project explores Row Echelon Form (REF) and Reduced Row Echelon
Form (RREF) as foundations for common linear-algebra operations.

## Covered concepts

- Gaussian elimination
- Gauss-Jordan elimination
- Partial pivoting
- Matrix rank
- Determinant tracking through row swaps
- Matrix inversion using an augmented identity matrix

## Implementation constraint

The Python implementation intentionally avoids high-level functions from
`numpy.linalg`. The goal is to expose the algorithmic steps instead of hiding
them behind library calls.

## Numerical note

Floating-point arithmetic is approximate. The implementation therefore uses a
small tolerance when deciding whether a potential pivot should be treated as
zero. Partial pivoting reduces, but does not eliminate, numerical error.
