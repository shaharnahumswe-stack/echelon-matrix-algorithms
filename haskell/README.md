# Haskell implementation

`Main.hs` contains the original Haskell implementation of Gaussian elimination,
rank, determinant, and inverse operations using the `hmatrix` package.

## Requirements

- GHC
- Cabal or Stack
- `hmatrix`

Example dependency installation with Cabal:

```bash
cabal update
cabal install hmatrix
```

The program reads matrix CSV paths interactively. This implementation is kept
alongside the tested Python package to demonstrate the same numerical ideas in
a functional language.

> The Haskell source was preserved from the academic project. The automated
> test suite in this repository currently covers the Python implementation.
