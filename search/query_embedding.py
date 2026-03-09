"""
Convert a natural language query into an embedding vector.

Uses the same Sentence Transformer model as the ingestion pipeline
to ensure the query and stored embeddings live in the same vector space.
"""

from ingestion.generate_embeddings import generate_embedding


def get_query_embedding(query_text):
    """
    Convert *query_text* into a 384-dimensional embedding.

    Parameters
    ----------
    query_text : str
        A natural language search query, e.g. "authentication logic".

    Returns
    -------
    list[float]
        384-dimensional embedding vector.
    """
    return generate_embedding(query_text)


if __name__ == "__main__":
    query = "login authentication"
    vec = get_query_embedding(query)
    print(f"Query: {query}")
    print(f"Embedding dimension: {len(vec)}")
    print(f"First 5 values: {vec[:5]}")
