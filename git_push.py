#!/usr/bin/env python3
"""
Push local main branch to GitHub remote repository.
Supports GITHUB_TOKEN environment variable or command-line token argument.
Usage:
  python git_push.py
  python git_push.py <your-github-personal-access-token>
"""
import os
import sys
import dulwich.porcelain as porcelain

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REMOTE = "https://github.com/Mohdfaiz05/techspec-site.git"

token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
if len(sys.argv) > 1 and sys.argv[1].strip():
    token = sys.argv[1].strip()

if token:
    target_remote = f"https://{token}@github.com/Mohdfaiz05/techspec-site.git"
    print("Using provided GitHub token for authentication...")
else:
    target_remote = "origin"
    print("Using standard origin remote URL...")

print(f"Pushing to {DEFAULT_REMOTE} (branch 'main')...")

try:
    porcelain.push(REPO_PATH, target_remote, "refs/heads/main")
    print("\n✅ SUCCESS: Pushed main branch to https://github.com/Mohdfaiz05/techspec-site.git")
except Exception as e:
    err_str = str(e)
    if "401" in err_str or "HTTPUnauthorized" in err_str:
        print("\n❌ AUTHENTICATION REQUIRED:")
        print("GitHub requires authentication to push to 'https://github.com/Mohdfaiz05/techspec-site.git'.")
        print("To push right now, either:")
        print("  1. Run with your GitHub Personal Access Token (PAT):")
        print("     python git_push.py <YOUR_GITHUB_TOKEN>")
        print("  2. Or set GITHUB_TOKEN environment variable:")
        print("     $env:GITHUB_TOKEN = '<YOUR_TOKEN>'; python git_push.py")
    else:
        print(f"\n❌ Push Error ({type(e).__name__}): {e}")
    sys.exit(1)
