#!/usr/bin/env python3
"""Python module for encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Return a salted hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks Hashed password against given password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
