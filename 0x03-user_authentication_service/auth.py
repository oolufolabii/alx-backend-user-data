#!/usr/bin/env python3

"""Python Auth module
"""
import bcrypt
from user import User


def _hash_password(password: str) -> str:
    """_hash_password method that takes in a password string
    arguments and returns bytes."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
