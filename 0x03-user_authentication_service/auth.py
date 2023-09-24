#!/usr/bin/env python3
'''auth module'''
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    '''Hashing a password'''
    return bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt())


def _generate_uuid() -> str:
    '''Generates a uuid string'''
    return uuid.uuid4().__str__()


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''Creates and saves a new User instance in the database if the email
        does not exist after hashing the password
        '''
        try:
            if self._db.find_user_by(email=email) is not None:
                raise ValueError(f'User {email} already exists')
            else:
                hashed_password = _hash_password(password)
                new_user = User(email=email, hashed_password=hashed_password)
                self._db._session.add(new_user)
                self._db._session.commit()
                return new_user
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = User(email=email, hashed_password=hashed_password)
            self._db._session.add(new_user)
            self._db._session.commit()
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        '''Checking if the arguments matches a user'''
        try:
            user = self._db.find_user_by(email=email)
            if user:
                hashed_password = user.hashed_password
                return bcrypt.checkpw(password.encode(), hashed_password)
        except Exception:
            return False
        return False

    def create_session(self, email: str) -> str:
        '''Creates a session'''
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                setattr(user, 'session_id', session_id)
                self._db._session.commit()
                return session_id
        except Exception:
            return None
        return None

    def get_user_from_session_id(self, session_id: str) -> User:
        '''Finds User by session ID'''
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user if user else None
