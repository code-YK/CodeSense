"""
Generate vector embeddings using Sentence Transformers.

Uses the all-MiniLM-L6-v2 model which produces 384-dimensional vectors.
The model instance is cached as a module-level singleton so it is only
loaded once regardless of how many times the functions are called.
"""

from sentence_transformers import SentenceTransformer
from config.db_config import EMBEDDING_MODEL_NAME


# -------------------------------------------------------------------
# Singleton model loader
# -------------------------------------------------------------------

_model = None


def _get_model():
    """Load (or return cached) Sentence Transformer model."""
    global _model
    if _model is None:
        print(f"  [*] Loading embedding model: {EMBEDDING_MODEL_NAME} ...")
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("  [✓] Model loaded.\n")
    return _model


# -------------------------------------------------------------------
# Public API
# -------------------------------------------------------------------

def generate_embedding(text):
    """
    Generate a single 384-dim embedding for the given text string.

    Returns
    -------
    list[float]
        A Python list of floats (length 384).
    """
    model = _get_model()
    embedding = model.encode(text)
    return embedding.tolist()


def generate_embeddings_batch(texts):
    """
    Generate embeddings for a list of text strings in one batch call.

    Parameters
    ----------
    texts : list[str]
        Code chunks or query strings.

    Returns
    -------
    list[list[float]]
        A list of 384-dim embedding vectors.
    """
    model = _get_model()
    embeddings = model.encode(texts, show_progress_bar=True)
    return [emb.tolist() for emb in embeddings]


if __name__ == "__main__":
    sample = "def authenticate_user(username, password): pass"
    vec = generate_embedding(sample)
    print(f"Embedding dimension: {len(vec)}")
    print(f"First 5 values: {vec[:5]}")
