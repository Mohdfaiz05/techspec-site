#!/usr/bin/env python3
"""
Initialize Git repository, stage files, and create initial commit.
"""
import os
import dulwich.porcelain as porcelain
from dulwich.repo import Repo

REPO_PATH = os.path.dirname(os.path.abspath(__file__))

print(f"Initializing repository at {REPO_PATH}...")
repo = porcelain.init(REPO_PATH)

print("Adding all files to index...")
porcelain.add(REPO_PATH)

print("Creating initial commit...")
commit_id = porcelain.commit(
    REPO_PATH,
    message=b"Initial commit: TechSpec India complete 490+ page SEO & affiliate static site",
    author=b"Mohdfaiz05 <faiz@techspec-site.pages.dev>",
    committer=b"Mohdfaiz05 <faiz@techspec-site.pages.dev>"
)

print(f"Commit created: {commit_id.decode() if isinstance(commit_id, bytes) else commit_id}")

# Set current branch to main
try:
    porcelain.branch_create(REPO_PATH, b"main")
    print("Created branch 'main'")
except Exception as e:
    print(f"Branch notice: {e}")

try:
    # Point HEAD to refs/heads/main
    repo.refs.set_symbolic_ref(b'HEAD', b'refs/heads/main')
    print("Set HEAD to refs/heads/main")
except Exception as e:
    print(f"Notice setting symbolic ref: {e}")

try:
    porcelain.remote_add(REPO_PATH, b"origin", b"https://github.com/Mohdfaiz05/techspec-site.git")
    print("Added remote origin: https://github.com/Mohdfaiz05/techspec-site.git")
except Exception as e:
    print(f"Remote notice: {e}")

print("Repository initialization and commit complete!")
