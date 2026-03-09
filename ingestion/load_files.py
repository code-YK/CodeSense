"""
Load code files from a local repository directory.

Recursively walks the directory tree using os.walk() and collects files
whose extensions match the supported list (.py, .js).
"""

import os
from config.db_config import SUPPORTED_EXTENSIONS


def load_code_files(directory, extensions=None):
    """
    Recursively scan *directory* for code files.

    Parameters
    ----------
    directory : str
        Path to the local repository folder.
    extensions : list[str] | None
        File extensions to include (with leading dot).
        Defaults to SUPPORTED_EXTENSIONS from config.

    Returns
    -------
    list[tuple[str, str]]
        A list of (file_path, file_content) tuples.
    """
    if extensions is None:
        extensions = SUPPORTED_EXTENSIONS

    code_files = []

    for root, _dirs, files in os.walk(directory):
        for filename in files:
            # Check if the file has a supported extension
            _, ext = os.path.splitext(filename)
            if ext.lower() in extensions:
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    code_files.append((file_path, content))
                    print(f"  [+] Loaded: {file_path}")
                except Exception as e:
                    print(f"  [!] Skipped {file_path}: {e}")

    print(f"\n  Total files loaded: {len(code_files)}")
    return code_files


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "./sample_repo"
    files = load_code_files(target)
    for path, content in files:
        print(f"\n--- {path} ({len(content)} chars) ---")
        print(content[:200])
