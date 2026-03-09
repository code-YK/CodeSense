# CodeSense — Semantic Code Search

A simple semantic search system that indexes code into vector embeddings and
uses **PostgreSQL + pgvector** for similarity search. Natural language queries
find relevant code — no keyword matching required.

---

## Tech Stack

| Layer        | Technology                        |
|-------------|-----------------------------------|
| Language    | Python 3.10+                      |
| Database    | PostgreSQL 15+ with pgvector      |
| Embeddings  | Sentence Transformers (all-MiniLM-L6-v2) |
| DB Driver   | psycopg2                          |

---

## Prerequisites

1. **PostgreSQL 15+** installed and running.
2. **pgvector extension** installed.  
   On most systems: `CREATE EXTENSION vector;` inside your database.
3. Create a database named `code_search`:
   ```sql
   CREATE DATABASE code_search;
   ```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure database (optional)

Defaults work for a local PostgreSQL installation. Override with env vars:

```bash
export CODESENSE_DB_HOST=localhost
export CODESENSE_DB_PORT=5432
export CODESENSE_DB_NAME=code_search
export CODESENSE_DB_USER=postgres
export CODESENSE_DB_PASSWORD=postgres
```

### 3. Ingest a code repository

```bash
python main.py ingest --repo-path ./sample_repo
```

This will:
- Initialize the database schema (creates the `code_chunks` table)
- Scan the folder for `.py` and `.js` files
- Chunk each file into meaningful pieces
- Generate 384-dim vector embeddings
- Store everything in PostgreSQL

### 4. Search with natural language

```bash
python main.py search --query "authentication logic"
python main.py search --query "payment processing" --limit 3
```

---

## Project Structure

```
CodeSense/
├── config/
│   └── db_config.py            # DB connection & model settings
├── database/
│   ├── connection.py           # psycopg2 connection helpers
│   └── schema.sql              # pgvector schema
├── ingestion/
│   ├── load_files.py           # Recursive file loader
│   ├── chunk_code.py           # Code chunking strategies
│   └── generate_embeddings.py  # Sentence Transformer wrapper
├── search/
│   ├── query_embedding.py      # Query → embedding
│   └── vector_search.py        # pgvector similarity search
├── scripts/
│   ├── ingest_repository.py    # Standalone ingestion CLI
│   └── search_cli.py           # Standalone search CLI
├── sample_repo/
│   ├── auth.py                 # Sample authentication module
│   └── payment.py              # Sample payment module
├── main.py                     # Unified CLI entry point
├── requirements.txt
└── README.md
```

---

## How It Works

1. **Load** — Recursively scan a local folder for `.py` / `.js` files.
2. **Chunk** — Split code by function / class definitions, or into fixed-size blocks.
3. **Embed** — Convert each chunk into a 384-dim vector using Sentence Transformers.
4. **Store** — Insert `(file_path, chunk_text, embedding)` into PostgreSQL.
5. **Search** — Embed the query, use pgvector's `<=>` cosine distance operator to find the closest chunks.

---

## Example

```
$ python main.py search --query "login authentication"

  Search Query: "login authentication"

  Converting query to embedding ...
  Searching database ...

  ═══════════════════  Results  ═══════════════════

  ── Result 1 (distance: 0.3421) ──
  File: sample_repo/auth.py

  def authenticate_user(username, password):
      ...
```

Even though the words *"login authentication"* don't appear in the code, semantic
search finds the relevant `authenticate_user` function.
