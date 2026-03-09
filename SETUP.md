# CodeSense — First Time Setup Guide

Follow these steps to set up and run the project for the first time.

---

## 1. Create and Activate Virtual Environment

```bash
python -m venv venv
```

**Activate (Windows):**
```bash
venv\Scripts\activate
```

**Activate (macOS/Linux):**
```bash
source venv/bin/activate
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Copy the example file and update with your PostgreSQL credentials:

```bash
cp .env.example .env
```

Edit `.env` with your database details:

```
CODESENSE_DB_HOST=localhost
CODESENSE_DB_PORT=5432
CODESENSE_DB_NAME=code_search
CODESENSE_DB_USER=postgres
CODESENSE_DB_PASSWORD=postgres
```

---

## 4. Set Up PostgreSQL Database

Open your PostgreSQL shell (`psql`) and run:

```sql
CREATE DATABASE code_search;
```

Then connect to the database and run the schema file:

```bash
psql -U postgres -d code_search -f database/schema.sql
```

Or manually inside `psql`:

```sql
\c code_search
\i database/schema.sql
```

This will enable the `pgvector` extension and create the `code_chunks` table.

---

## 5. Ingest Sample Repository

```bash
python main.py ingest --repo-path ./sample_repo
```

This will:
- Initialize the database schema
- Scan `sample_repo/` for `.py` and `.js` files
- Chunk each file into meaningful pieces
- Generate 384-dim vector embeddings
- Store everything in PostgreSQL

---

## 6. Search with Natural Language

```bash
python main.py search --query "authentication logic"
```

Try other queries:

```bash
python main.py search --query "payment processing"
python main.py search --query "password hashing"
python main.py search --query "invoice generation"
python main.py search --query "credit card validation" --limit 3
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `python main.py ingest --repo-path <path>` | Ingest a local code repository |
| `python main.py search --query "<query>"` | Search with natural language |
| `python main.py search --query "<query>" --limit N` | Limit number of results |
| `python scripts/ingest_repository.py <path>` | Standalone ingestion script |
| `python scripts/search_cli.py "<query>"` | Standalone search script |
