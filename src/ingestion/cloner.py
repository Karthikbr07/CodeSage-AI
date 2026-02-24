import os
import shutil
import tempfile
from git import Repo

# Clones a GitHub repo and returns the local path.
# Creates a temp directory so we don't pollute the filesystem.
def clone_repo( github_url: str) -> str:
    tmp_dir = tempfile.mkdtemp()
    print(f"Cloning {github_url} into {tmp_dir}...")
    Repo.clone_from(github_url, tmp_dir)
    print("Clone complete.")
    return tmp_dir

def cleanup_repo(local_path: str):
    """Remove the cloned repo after we're done processing."""
    shutil.rmtree(local_path, ignore_errors=True)
    