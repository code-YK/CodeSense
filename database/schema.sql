-- ============================================================
-- CodeSense Database Schema
-- ============================================================
-- Enables the pgvector extension and creates the table used to
-- store code chunks alongside their vector embeddings.
-- ============================================================

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop existing table if re-initializing
DROP TABLE IF EXISTS code_chunks;

-- Main storage table
CREATE TABLE code_chunks (
    id SERIAL PRIMARY KEY,
    file_path TEXT NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding VECTOR (384) NOT NULL
);

-- Index for faster cosine-distance searches
CREATE INDEX ON code_chunks USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);