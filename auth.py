"""
auth.py - Password hashing and user authentication
Uses hashlib (SHA-256 + salt) since bcrypt may not be installed.
Cyber-Attack Simulator & Defense Lab
"""

import hashlib
import os
import database as db


def _hash_password(password: str) -> str:
    """Hash a password with a random salt. Returns 'salt:hash'."""
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"


def _verify_password(password: str, stored: str) -> bool:
    """Verify a plaintext password against a stored 'salt:hash'."""
    try:
        salt, hashed = stored.split(":")
        return hashlib.sha256((salt + password).encode()).hexdigest() == hashed
    except ValueError:
        return False


def register_user(username: str, password: str) -> dict:
    """
    Register a new user. Returns {'success': bool, 'message': str, 'user': dict|None}.
    """
    if not username or len(username) < 3:
        return {"success": False, "message": "Username must be at least 3 characters.", "user": None}
    if not password or len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters.", "user": None}
    if not username.replace("_", "").isalnum():
        return {"success": False, "message": "Username can only contain letters, numbers, underscores.", "user": None}

    pw_hash = _hash_password(password)
    created = db.create_user(username, pw_hash)
    if not created:
        return {"success": False, "message": "Username already taken. Please choose another.", "user": None}

    user = db.get_user(username)
    return {"success": True, "message": "Account created! You can now log in.", "user": user}


def login_user(username: str, password: str) -> dict:
    """
    Authenticate a user. Returns {'success': bool, 'message': str, 'user': dict|None}.
    """
    user = db.get_user(username)
    if not user:
        return {"success": False, "message": "Username not found.", "user": None}
    if not _verify_password(password, user["password_hash"]):
        return {"success": False, "message": "Incorrect password.", "user": None}
    return {"success": True, "message": "Login successful.", "user": user}
