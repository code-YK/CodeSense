"""
CodeSense — Semantic Code Search using PostgreSQL & pgvector.

Unified CLI entry point with two sub-commands:

    python main.py ingest  --repo-path ./sample_repo
    python main.py search  --query "authentication logic"
"""

import argparse
import sys
import os

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(__file__))


def cmd_ingest(args):
    """Handle the 'ingest' sub-command."""
    from scripts.ingest_repository import ingest

    if not os.path.isdir(args.repo_path):
        print(f"Error: '{args.repo_path}' is not a valid directory.")
        sys.exit(1)

    ingest(args.repo_path)


def cmd_search(args):
    """Handle the 'search' sub-command."""
    from scripts.search_cli import search

    search(args.query, limit=args.limit)


def main():
    parser = argparse.ArgumentParser(
        prog="CodeSense",
        description="Semantic Code Search using PostgreSQL & pgvector",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ── ingest ────────────────────────────────────────────────────
    ingest_parser = subparsers.add_parser(
        "ingest",
        help="Ingest a local code repository into the vector database.",
    )
    ingest_parser.add_argument(
        "--repo-path",
        required=True,
        help="Path to the local repository folder (e.g. ./sample_repo)",
    )
    ingest_parser.set_defaults(func=cmd_ingest)

    # ── search ────────────────────────────────────────────────────
    search_parser = subparsers.add_parser(
        "search",
        help="Search indexed code using a natural language query.",
    )
    search_parser.add_argument(
        "--query",
        required=True,
        help='Natural language query (e.g. "authentication logic")',
    )
    search_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of results to return (default: 5)",
    )
    search_parser.set_defaults(func=cmd_search)

    # ── parse & dispatch ──────────────────────────────────────────
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
