#!/usr/bin/env python3

"""Python Auth module
"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> str:
    """_hash_password method that takes in a password string
    arguments and returns bytes."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """take mandatory email and password string arguments
        and return a User object."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)
            return user
        else:
            raise ValueError('User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """Validate credentials, return true or false"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(password=password.encode('utf-8'),
                                  hashed_password=user.hashed_password)

    def create_session(self, email: str) -> str:
        """Return the session ID as a string format"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        else:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """Return a user or None"""
        try:
            user = self._db.find_user_by(session_id=session_id)

        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """This method updates the corresponding user
        session ID to None"""

        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Use the reset_token to find the corresponding user.
        If it does not exist, raise a ValueError exception."""

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        passwd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=passwd, reset_token=None)
