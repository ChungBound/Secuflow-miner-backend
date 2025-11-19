#!/bin/bash

# 检查输入参数
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 REPO_PATH BRANCH"
    exit 1
fi

# 接收命令行参数
REPO_PATH="$1"
BRANCH="$2"

./run.sh "FileDependencyMatrixMiner" --repository "$REPO_PATH" "$BRANCH"
./run.sh "AssignmentMatrixMiner" --repository "$REPO_PATH" "$BRANCH"
./run.sh "ChangedFilesMiner" --repository "$REPO_PATH" "$BRANCH"