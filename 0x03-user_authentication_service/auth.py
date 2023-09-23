#!/usr/bin/env python3
'''auth module'''
import bcrypt


def _hash_password(password: str) -> bytes:
    '''Hashing a password'''
    return bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt())
