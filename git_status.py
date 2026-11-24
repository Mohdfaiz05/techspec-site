#!/usr/bin/env python3
import os
import dulwich.porcelain as porcelain

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
status = porcelain.status(REPO_PATH)
print("Staged:", status.staged)
print("Unstaged:", status.unstaged)
print("Untracked:", len(status.untracked), "untracked files")
