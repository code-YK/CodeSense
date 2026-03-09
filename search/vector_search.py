"""
Vector similarity search against the code_chunks table.

Uses the pgvector <=> (cosine distance) operator to find the most
relevant code snippets for a given query embedding.
"""

from database.connection import get_connection


def search_similar_code(query_embedding, limit=5):
    """
    Find the *limit* most similar code chunks to *query_embedding*.

    Parameters
    ----------
    query_embedding : list[float]
        384-dimensional embedding of the search query.
    limit : int
        Maximum number of results to return.

    Returns
    -------
    list[dict]
        Each dict contains: id, file_path, chunk_text, distance.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, file_path, chunk_text,
                       embedding <=> %s::vector AS distance
                FROM   code_chunks
                ORDER  BY embedding <=> %s::vector
                LIMIT  %s;
                """,
                (str(query_embedding), str(query_embedding), limit),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "file_path": row[1],
            "chunk_text": row[2],
            "distance": round(float(row[3]), 4),
        })
    return results


def format_results(results):
    """
    Pretty-print search results for CLI display.

    Parameters
    ----------
    results : list[dict]
        Output of search_similar_code().

    Returns
    -------
    str
        Formatted string ready for printing.
    """
    if not results:
        return "  No results found."

    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"  ── Result {i} (distance: {r['distance']}) ──")
        lines.append(f"  File: {r['file_path']}\n")
        lines.append(f"{r['chunk_text']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    from search.query_embedding import get_query_embedding

    query = "authentication logic"
    emb = get_query_embedding(query)
    results = search_similar_code(emb)
    print(format_results(results))
