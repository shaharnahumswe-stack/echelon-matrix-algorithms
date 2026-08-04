"""Command-line interface for the echelon-matrix package."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .core import determinant, inverse, matrix_rank, row_echelon_form


def _load_csv(path: Path) -> np.ndarray:
    try:
        matrix = np.loadtxt(path, delimiter=",")
    except OSError as exc:
        raise SystemExit(f"Could not read '{path}': {exc}") from exc
    except ValueError as exc:
        raise SystemExit(f"Invalid CSV matrix in '{path}': {exc}") from exc

    if matrix.ndim == 1:
        matrix = np.atleast_2d(matrix)
    return matrix


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="echelon-matrix",
        description="Compute REF, rank, determinant, or inverse from a CSV matrix.",
    )
    parser.add_argument("operation", choices=("ref", "rank", "det", "inverse"))
    parser.add_argument("csv_file", type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    matrix = _load_csv(args.csv_file)

    if args.operation == "ref":
        ref, rank, swaps = row_echelon_form(matrix)
        print(ref)
        print(f"rank={rank}, row_swaps={swaps}")
    elif args.operation == "rank":
        print(matrix_rank(matrix))
    elif args.operation == "det":
        print(determinant(matrix))
    else:
        result = inverse(matrix)
        if result is None:
            raise SystemExit("Matrix is singular; inverse does not exist.")
        print(result)


if __name__ == "__main__":
    main()
