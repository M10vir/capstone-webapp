#!/bin/bash

REPO_DIR="/c/LabFiles/Capstone-Project"
BRANCH="main"
COMMIT_MSG="Automated push from approval workflow"

cd "$REPO_DIR" || exit

git add .
git commit -m "$COMMIT_MSG"
git push origin "$BRANCH"