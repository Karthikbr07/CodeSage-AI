# src/ingestion/parser.py
import os
from typing import List, Dict

# File extensions we care about
SUPPORTED_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp',
    '.c', '.cs', '.go', '.rs', '.rb', '.php', '.swift',
    '.kt', '.md', '.json', '.yaml', '.yml', '.toml', '.env.example'
}

def get_all_files(repo_path: str) -> List[str]:
    """Walk through the repo and collect all supported code files."""
    files = []
    skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}
    
    for root, dirs, filenames in os.walk(repo_path):
        # Skip irrelevant directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                files.append(os.path.join(root, filename))
    
    return files

def chunk_file(file_path: str, repo_path: str, chunk_size: int = 60, overlap: int = 10) -> List[Dict]:
    """
    Read a file and split it into overlapping chunks.
    
    chunk_size: number of lines per chunk
    overlap: lines shared between consecutive chunks (so we don't cut logic in half)
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        return []
    
    if not lines:
        return []
    
    chunks = []
    relative_path = os.path.relpath(file_path, repo_path)
    
    start = 0
    while start < len(lines):
        end = min(start + chunk_size, len(lines))
        chunk_text = ''.join(lines[start:end])
        
        chunks.append({
            'content': chunk_text,
            'metadata': {
                'file_path': relative_path,
                'start_line': start + 1,  # 1-indexed for humans
                'end_line': end,
                'language': get_language(file_path)
            }
        })
        
        # Move forward but keep 'overlap' lines from the previous chunk
        start += chunk_size - overlap
    
    return chunks

def get_language(file_path: str) -> str:
    ext_map = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
        '.java': 'Java', '.cpp': 'C++', '.go': 'Go', '.rs': 'Rust',
        '.rb': 'Ruby', '.php': 'PHP', '.cs': 'C#'
    }
    ext = os.path.splitext(file_path)[1].lower()
    return ext_map.get(ext, 'Unknown')

def parse_repo(repo_path: str) -> List[Dict]:
    """Main function: parse all files in a repo into chunks."""
    all_files = get_all_files(repo_path)
    all_chunks = []
    
    for file_path in all_files:
        chunks = chunk_file(file_path, repo_path)
        all_chunks.extend(chunks)
    
    print(f"Parsed {len(all_files)} files into {len(all_chunks)} chunks.")
    return all_chunks