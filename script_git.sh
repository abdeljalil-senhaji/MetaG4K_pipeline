#!/bin/bash

PROJET_NAME=$1
GITHUB_REPO_URL=$2

mkdir -p "$PROJET_NAME"
cd "$PROJET_NAME" || exit

git init
#git config --local user.name "ton_pseudo"
#git config --local user.email "ton_email@example.com"

echo "# $PROJET_NAME" > README.md
touch script.py

git add .
git commit -m "Initial commit"

git remote add origin "$GITHUB_REPO_URL"
git branch -M main
git push -u origin main




# test :
#...sh name_project https://github.com/tonpseudo/name_project.git 
