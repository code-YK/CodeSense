"""
Ingest a local code repository into the CodeSense vector database.

Usage:
    python scripts/ingest_repository.py <repo_path>

Example:
    python scripts/ingest_repository.py ./sample_repo

The script will:
  1. Recursively scan the folder for .py and .js files.
  2. Chunk each file into meaningful pieces.
  3. Generate 384-dim embeddings for every chunk.
  4. Store file_path, chunk_text, and embedding in PostgreSQL.
"""

import sys
import os

# Ensure project root is on sys.path so absolute imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ingestion.load_files import load_code_files
from ingestion.chunk_code import chunk_file
from ingestion.generate_embeddings import generate_embeddings_batch
from database.connection import get_connection, initialize_database


def ingest(repo_path):
    """
    Full ingestion pipeline for a local repository.

    Parameters
    ----------
    repo_path : str
        Path to the local code repository folder.
    """
    # ── 0. Bootstrap DB schema ────────────────────────────────────
    print("\n[1/4] Initializing database schema ...")
    initialize_database()

    # ── 1. Load files ─────────────────────────────────────────────
    print(f"\n[2/4] Scanning repository: {repo_path}")
    files = load_code_files(repo_path)

    if not files:
        print("  No supported code files found. Exiting.")
        return

    # ── 2. Chunk files ────────────────────────────────────────────
    print("\n[3/4] Chunking code files ...")
    all_chunks = []          # list of (file_path, chunk_text)
    for file_path, content in files:
        chunks = chunk_file(file_path, content)
        for chunk in chunks:
            all_chunks.append((file_path, chunk))

    print(f"  Total chunks created: {len(all_chunks)}")

    if not all_chunks:
        print("  No chunks generated. Exiting.")
        return

    # ── 3. Generate embeddings ────────────────────────────────────
    print("\n[4/4] Generating embeddings ...")
    chunk_texts = [text for _, text in all_chunks]
    embeddings = generate_embeddings_batch(chunk_texts)

    # ── 4. Store in PostgreSQL ────────────────────────────────────
    print("\n  Inserting into database ...")
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for (file_path, chunk_text), embedding in zip(all_chunks, embeddings):
                cur.execute(
                    """
                    INSERT INTO code_chunks (file_path, chunk_text, embedding)
                    VALUES (%s, %s, %s::vector);
                    """,
                    (file_path, chunk_text, str(embedding)),
                )
        conn.commit()
        print(f"  [✓] Successfully inserted {len(all_chunks)} chunks.\n")
    except Exception as e:
        conn.rollback()
        print(f"  [✗] Database insertion failed: {e}")
        raise
    finally:
        conn.close()


# ── CLI entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/ingest_repository.py <repo_path>")
        print("Example: python scripts/ingest_repository.py ./sample_repo")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not os.path.isdir(repo_path):
        print(f"Error: '{repo_path}' is not a valid directory.")
        sys.exit(1)

    ingest(repo_path)
