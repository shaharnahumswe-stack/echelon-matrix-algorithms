# Echelon Matrix Algorithms

A compact scientific-programming project that implements core linear-algebra
operations from first principles using **Gaussian elimination** and
**Gauss-Jordan elimination**.

The repository includes a tested Python package and the original Haskell
implementation. High-level `numpy.linalg` functions are intentionally avoided
in the Python algorithms so the elimination process remains visible.

## What it computes

- Row Echelon Form (REF)
- Matrix rank, including rectangular matrices
- Determinant of a square matrix
- Inverse of a nonsingular square matrix
- Partial pivoting for improved numerical stability

## Repository structure

```text
.
├── src/echelon_matrix/   # Tested Python implementation and CLI
├── tests/                # Pytest test suite
├── examples/             # Example CSV matrix
├── haskell/              # Original Haskell implementation
└── docs/                 # Short mathematical and design summary
```

## Quick start

```bash
git clone https://github.com/<your-username>/echelon-matrix.git
cd echelon-matrix
python -m venv .venv
```

Activate the environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install the package and development dependencies:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

Run the tests:

```bash
pytest
```

## Python usage

```python
import numpy as np

from echelon_matrix import determinant, inverse, matrix_rank

matrix = np.array(
    [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 10.0],
    ]
)

print(determinant(matrix))  # -3.0
print(matrix_rank(matrix))  # 3
print(inverse(matrix))
```

## Command-line usage

After installation, run an operation on a comma-separated matrix file:

```bash
echelon-matrix det examples/matrix.csv
echelon-matrix rank examples/matrix.csv
echelon-matrix inverse examples/matrix.csv
echelon-matrix ref examples/matrix.csv
```

## Algorithm outline

### Rank and determinant

1. Select a pivot using partial pivoting.
2. Swap rows when necessary.
3. Eliminate entries below the pivot.
4. Count pivots to obtain rank.
5. For square full-rank matrices, multiply diagonal pivots and adjust the sign
   according to the number of row swaps.

### Inverse

1. Construct the augmented matrix `[A | I]`.
2. Apply Gauss-Jordan elimination until the left side becomes the identity.
3. Return the right side as `A⁻¹`.
4. If a valid pivot cannot be found, the matrix is singular.

## Complexity

For an `n × n` matrix, determinant and inverse computations use cubic time in
the standard dense case: **O(n³)**. The algorithms use **O(n²)** memory.

## Notes

- Floating-point results are approximate.
- A tolerance is used when deciding whether a pivot is effectively zero.
- The implementation is educational and is not a replacement for mature
  numerical libraries in production scientific workloads.

## Authors

- Shahar Nahum
- Arad Harush

This project was originally developed as part of a scientific-programming
course and was later reorganized into a portfolio-ready repository.
