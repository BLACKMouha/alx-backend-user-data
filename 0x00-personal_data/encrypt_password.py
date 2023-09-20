#!/usr/bin/env python3
'''encrypt_password module'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''Encrypts a password'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''Checks if the hashed password and the password are identical'''
    return bcrypt.checkpw(password.encode(), hashed_password)
