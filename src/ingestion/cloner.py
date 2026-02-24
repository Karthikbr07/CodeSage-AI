import os
import shutil
import tempfile
from git import Repo

# Clones a GitHub repo and returns the local path.
# Creates a temp directory so we don't pollute the filesystem.
def clone_repo( github_url: str) -> str:
    
    tmp_dir = tempfile.mkdtemp() # tempfile is a inbuilt method of python. mkdtemp() creates a temporary directory and returns its path. The directory is created in the default location for temporary files on the system, and it is automatically cleaned up when the program exits.
    print(f"Cloning {github_url} into {tmp_dir}...")
    Repo.clone_from(github_url, tmp_dir)  # Repo is a class from the GitPython library . The clone_from method is used to clone a repository from a specified URL (github_url) into a local directory (tmp_dir).
    # this is equivlaent to running ---> git clone <github_url> <tmp_dir>`
    print("Clone complete.")
    return tmp_dir

def cleanup_repo(local_path: str):
    """Remove the cloned repo after we're done processing."""
    shutil.rmtree(local_path, ignore_errors=True)
    