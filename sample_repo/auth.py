"""
Sample authentication module for CodeSense demo.

Contains typical user authentication functions that the semantic search
engine should be able to discover using queries like:
  - "authentication logic"
  - "login validation"
  - "password hashing"
  - "session management"
"""

import hashlib
import secrets
import time


# ── In-memory session store (demo purposes only) ─────────────────
_active_sessions = {}


def authenticate_user(username, password):
    """
    Authenticate a user by verifying their credentials.

    In a real application this would check against a database.
    For this demo it uses a hard-coded admin account.
    """
    # Demo credentials — replace with proper DB lookup in production
    valid_users = {
        "admin": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
        "user1": "6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090",
    }

    password_hash = hash_password(password)

    if username in valid_users and valid_users[username] == password_hash:
        session = create_session(username)
        return {"success": True, "session_token": session}

    return {"success": False, "error": "Invalid credentials"}


def hash_password(password):
    """
    Hash a password using SHA-256.

    For production, use bcrypt or argon2 instead of plain SHA-256.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_session(username):
    """
    Create a new session token for an authenticated user.

    Returns a secure random hex token and stores it with an expiry
    timestamp in the in-memory session store.
    """
    token = secrets.token_hex(32)
    _active_sessions[token] = {
        "username": username,
        "created_at": time.time(),
        "expires_at": time.time() + 3600,  # 1-hour expiry
    }
    return token


def validate_token(token):
    """
    Validate a session token.

    Returns the associated username if the token is valid and has not
    expired, otherwise returns None.
    """
    session = _active_sessions.get(token)
    if session is None:
        return None

    if time.time() > session["expires_at"]:
        # Token has expired — clean it up
        del _active_sessions[token]
        return None

    return session["username"]


def logout(token):
    """Invalidate a session token by removing it from the store."""
    if token in _active_sessions:
        del _active_sessions[token]
        return True
    return False
