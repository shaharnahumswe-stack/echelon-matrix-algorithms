@echo off
setlocal

where git >nul 2>nul
if errorlevel 1 (
    echo Git is not installed or is not available in PATH.
    echo Install Git for Windows from: https://git-scm.com/download/win
    echo Then close this window and run this file again.
    pause
    exit /b 1
)

cd /d "%~dp0"

if not exist ".git" git init

git add .
git commit -m "Initial portfolio-ready project structure"

git branch -M main

git remote get-url origin >nul 2>nul
if errorlevel 1 (
    git remote add origin https://github.com/shaharnahumswe-stack/echelon-matrix-algorithms.git
) else (
    git remote set-url origin https://github.com/shaharnahumswe-stack/echelon-matrix-algorithms.git
)

git push -u origin main

echo.
echo Finished. If GitHub asks you to sign in, complete the browser sign-in and run this file again.
pause
