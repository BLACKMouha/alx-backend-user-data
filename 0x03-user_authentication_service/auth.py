#!/usr/bin/env python3
'''auth module'''
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    '''Hashing a password'''
    return bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
        self.__session = self._db._session

    def register_user(self, email: str, password: str) -> User:
        '''Creates and saves a new User instance in the database if the email
        does not exist after hashing the password
        '''
        if self._db.find_user_by(email=email) is not None:
            raise ValueError(f'User {email} already exists')
        hashed_password = _hash_password(password)
        new_user = User(email=email, hashed_password=hashed_password)
        self.__session.add(new_user)
        self.__session.commit()
        return new_user
