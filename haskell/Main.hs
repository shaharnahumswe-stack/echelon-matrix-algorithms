{-# LANGUAGE FlexibleContexts #-}

module Main where

import Numeric.LinearAlgebra
    ( Matrix, Vector
    , fromLists, fromRows, toRows, toList
    , rows, cols, (!), scale, (===), ident, (|||)
    , subVector
    )


import System.CPUTime
import Text.Read (readMaybe)
import Data.Maybe (mapMaybe)
import Data.List (maximumBy)
import Data.Ord (comparing)
import Control.Monad (forM_)
import Text.Printf (printf)


timeIt :: String -> IO a -> IO (a, Double)
timeIt label action = do
    start <- getCPUTime
    result <- action
    end <- getCPUTime
    let diff = fromIntegral (end - start) / 1e12
    putStrLn $ label ++ " took " ++ show diff ++ " s"
    return (result, diff)


parseLine :: String -> Maybe [Double]
parseLine line = mapM readMaybe $ words $ map (\c -> if c == ',' then ' ' else c) line

readMatrix :: FilePath -> IO (Either String (Matrix Double))
readMatrix path = do
    content <- readFile path
    let ls = lines content
    case traverse parseLine ls of
        Nothing   -> return $ Left "Parse error"
        Just rows -> return $ Right $ fromLists rows


swapRows :: Int -> Int -> [Vector Double] -> [Vector Double]
swapRows i j rs
    | i == j = rs
    | otherwise =
        let ri = rs !! i
            rj = rs !! j
            replace idx r
              | idx == i = rj
              | idx == j = ri
              | otherwise = r
        in zipWith replace [0..] rs


elimColumn :: Int -> Double -> [Vector Double] -> [Vector Double]
elimColumn k pivot rs =
    let n = length rs
        rk = rs !! k
        go i r
          | i <= k = r
          | otherwise =
              let factor = (r ! k) / pivot
              in r - scale factor rk
    in zipWith go [0..n-1] rs



gaussianElim :: Matrix Double -> (Matrix Double, Int)
gaussianElim a =
    let n = rows a
        rs0 = toRows a          
        (finalRows, sign) = go 0 1 rs0
    in (fromRows finalRows, sign)
  where
    n = rows a
    go k sign rs
        | k >= n = (rs, sign)
        | otherwise =
            let nrows = length rs
                candidates = [k .. nrows - 1]
                pivotRow = maximumBy (comparing (\i -> abs $ (rs !! i) ! k)) candidates
                pivotVal = (rs !! pivotRow) ! k
            in if abs pivotVal < 1e-12
               then 
                    go (k + 1) sign rs
               else
                   let rsSwapped = if pivotRow /= k then swapRows k pivotRow rs else rs
                       sign' = if pivotRow /= k then -sign else sign
                       pivotNow = (rsSwapped !! k) ! k
                       rsElim = elimColumn k pivotNow rsSwapped
                   in go (k + 1) sign' rsElim


computeRank :: Matrix Double -> Int
computeRank a =
    let (u, _) = gaussianElim a
        n = min (rows a) (cols a)
        ur = toRows u
        diagVals = [ ur !! i ! i | i <- [0 .. n - 1] ]
    in length $ filter (\x -> abs x > 1e-10) diagVals

computeDeterminant :: Matrix Double -> Double
computeDeterminant a
    | rows a /= cols a = error "Determinant only for square matrices"
    | otherwise =
        let (u, sign) = gaussianElim a
            n = rows a
            ur = toRows u
            diagVals = [ ur !! i ! i | i <- [0 .. n - 1] ]
        in fromIntegral sign * product diagVals


computeInverse :: Matrix Double -> Maybe (Matrix Double)
computeInverse a
    | rows a /= cols a = Nothing
    | otherwise = gaussJordan a

gaussJordan :: Matrix Double -> Maybe (Matrix Double)
gaussJordan a =
    let n = rows a
        aug = toRows (a ||| ident n)
    in fmap extractInverse (elim 0 aug)
  where
    n = rows a

    elim :: Int -> [Vector Double] -> Maybe [Vector Double]
    elim k rs
        | k >= n = Just rs
        | otherwise =
            let nrows = length rs
                candidates = [k .. nrows - 1]
                pivotRow = maximumBy (comparing (\i -> abs $ (rs !! i) ! k)) candidates
                pivotVal = (rs !! pivotRow) ! k
            in if abs pivotVal < 1e-12
               then Nothing
               else
                   let rsSwapped = if pivotRow /= k then swapRows k pivotRow rs else rs
                       pivot = (rsSwapped !! k) ! k
                       rowK = rsSwapped !! k
                       rowKnorm = scale (1 / pivot) rowK
                       replaceRow i r
                         | i == k = rowKnorm
                         | otherwise =
                             let factor = r ! k
                             in r - scale factor rowKnorm
                       rs' = zipWith replaceRow [0 .. (nrows - 1)] rsSwapped
                   in elim (k + 1) rs'

    extractInverse :: [Vector Double] -> Matrix Double
    extractInverse rs = fromRows $ map (\r -> subVector n n r) rs

printMatrix :: Matrix Double -> IO ()
printMatrix m = do
    let rs = toRows m
    forM_ rs $ \r ->
        putStrLn . unwords . map (printf "%.6f") $ toList r


main :: IO ()
main = do
    putStrLn "Enter CSV for Rank:"
    fileR <- getLine
    eMatR <- readMatrix fileR
    case eMatR of
        Left err -> putStrLn err
        Right mat -> do
            _ <- timeIt "Rank" $ print (computeRank mat)
            return ()

    putStrLn "Enter CSV for Determinant:"
    fileD <- getLine
    eMatD <- readMatrix fileD
    case eMatD of
        Left err -> putStrLn err
        Right mat -> do
            _ <- timeIt "Determinant" $ print (computeDeterminant mat)
            return ()

    putStrLn "Enter CSV for Inverse:"
    fileI <- getLine
    eMatI <- readMatrix fileI
    case eMatI of
        Left err -> putStrLn err
        Right mat -> do
            (invResult, _) <- timeIt "Inverse" $
                return (computeInverse mat)
            case invResult of
                Nothing     -> putStrLn "Matrix is singular, no inverse."
                Just invMat -> do
                    putStrLn "Inverse matrix:"
                    printMatrix invMat
