import os
from git import Repo
from pathlib import Path

def clone_repo(repo_url, dest_dir):
  if not os.path.exists(dest_dir):
    print(f"Cloning {repo_url} to {dest_dir}")
    Repo.clone_from(repo_url, dest_dir)
    print("Repo cloned")
  else:
    print("Repo already cloned")

def list_code_files(base_path, exts=None):
    exts = exts or [".py", ".js", ".ts", ".java", ".go", ".md", ".html", ".css"]
    for path in Path(base_path).rglob("*"):
        if path.is_file() and path.suffix in exts:
            yield path

if __name__ == "__main__":
  repo_url = input("Enter the repo URL: ")
  dest_dir = input("Enter the destination directory: ")
  clone_repo(repo_url, dest_dir)