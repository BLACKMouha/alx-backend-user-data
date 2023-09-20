#!/usr/bin/env python3
'''encrypt_password module'''

from bcrypt import hashpw, gensalt


def hash_password(password: str) -> bytes:
    '''Encrypts a password'''
    return hashpw(password.encode('utf-8'), gensalt())
