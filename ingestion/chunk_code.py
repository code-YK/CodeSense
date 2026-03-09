"""
Code chunking strategies for CodeSense.

Provides two chunking approaches:
  1. Function-based  – splits Python code by def / class definitions.
  2. Fixed-size       – splits any text into overlapping character blocks.

The main entry point, chunk_file(), tries function-based chunking first
and falls back to fixed-size when no meaningful splits are found.
"""

import re


# ---------------------------------------------------------------------------
# Strategy 1: Function / Class based chunking (Python-specific)
# ---------------------------------------------------------------------------

def chunk_by_functions(code_text):
    """
    Split Python source code into chunks at the top-level function
    and class boundaries.

    Returns a list of code strings, one per function/class.  If the
    regex finds no definitions the list will be empty.
    """
    # Pattern matches top-level def/class (no leading whitespace)
    pattern = r"^(?=(?:def |class ))"
    parts = re.split(pattern, code_text, flags=re.MULTILINE)

    # Filter out empty / whitespace-only fragments
    chunks = [part.strip() for part in parts if part.strip()]
    return chunks


# ---------------------------------------------------------------------------
# Strategy 2: Fixed-size chunking with overlap
# ---------------------------------------------------------------------------

def chunk_fixed_size(code_text, chunk_size=512, overlap=50):
    """
    Split *code_text* into character blocks of *chunk_size* with the
    specified *overlap* between consecutive blocks.
    """
    chunks = []
    start = 0
    text_length = len(code_text)

    while start < text_length:
        end = start + chunk_size
        chunk = code_text[start:end]
        if chunk.strip():            # skip empty chunks
            chunks.append(chunk.strip())
        start += chunk_size - overlap

    return chunks


# ---------------------------------------------------------------------------
# Primary entry point
# ---------------------------------------------------------------------------

def chunk_file(file_path, content, chunk_size=512, overlap=50):
    """
    Chunk a single source file.

    For Python files the function first attempts to split by function /
    class definitions.  If that produces fewer than 2 chunks the code
    falls back to fixed-size splitting.

    Parameters
    ----------
    file_path : str
        Path of the source file (used to decide strategy).
    content : str
        Full text content of the file.
    chunk_size : int
        Character count for fixed-size chunks.
    overlap : int
        Number of overlapping characters between consecutive chunks.

    Returns
    -------
    list[str]
        A list of code chunk strings.
    """
    if not content.strip():
        return []

    # Try function-based chunking for Python files
    if file_path.endswith(".py"):
        chunks = chunk_by_functions(content)
        if len(chunks) >= 2:
            return chunks

    # Fallback: fixed-size chunking
    return chunk_fixed_size(content, chunk_size, overlap)


if __name__ == "__main__":
    sample = '''
def hello():
    print("hello")

def world():
    print("world")

class Greeter:
    def greet(self):
        print("hi")
'''
    chunks = chunk_file("demo.py", sample)
    for i, c in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} ---")
        print(c)
