"""
Search the CodeSense vector database with a natural language query.

Usage:
    python scripts/search_cli.py "<query>"

Example:
    python scripts/search_cli.py "authentication logic"
    python scripts/search_cli.py "payment processing"

The script will:
  1. Convert the query into a 384-dim embedding.
  2. Perform cosine-distance similarity search against stored code chunks.
  3. Display the top matching code snippets.
"""

import sys
import os

# Ensure project root is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from search.query_embedding import get_query_embedding
from search.vector_search import search_similar_code, format_results


def search(query_text, limit=5):
    """
    Run a semantic search for *query_text*.

    Parameters
    ----------
    query_text : str
        Natural language search query.
    limit : int
        Number of results to return.
    """
    print(f'\n  Search Query: "{query_text}"\n')

    # ── 1. Embed the query ────────────────────────────────────────
    print("  Converting query to embedding ...")
    query_embedding = get_query_embedding(query_text)

    # ── 2. Vector similarity search ───────────────────────────────
    print("  Searching database ...\n")
    results = search_similar_code(query_embedding, limit=limit)

    # ── 3. Display results ────────────────────────────────────────
    print("  ═══════════════════  Results  ═══════════════════\n")
    print(format_results(results))


# ── CLI entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python scripts/search_cli.py "<query>"')
        print('Example: python scripts/search_cli.py "authentication logic"')
        sys.exit(1)

    query_text = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    search(query_text, limit)
