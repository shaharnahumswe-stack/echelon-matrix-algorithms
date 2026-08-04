# Uploading this project to GitHub

## 1. Install Git for Windows

Install Git from the official Git website:

`https://git-scm.com/download/win`

The default installation options are suitable.

## 2. Make sure the GitHub repository is empty

Repository:

`https://github.com/shaharnahumswe-stack/echelon-matrix-algorithms`

If you already committed the flattened browser upload, the cleanest option is to delete and recreate the repository with the same name.

## 3. Push automatically

Double-click:

`push-to-github.bat`

The script initializes Git, creates the first commit, connects the repository, and pushes the `main` branch.

GitHub may open a browser window and ask you to sign in.

## Manual alternative

Open Git Bash in this folder and run:

```bash
git init
git add .
git commit -m "Initial portfolio-ready project structure"
git branch -M main
git remote add origin https://github.com/shaharnahumswe-stack/echelon-matrix-algorithms.git
git push -u origin main
```
