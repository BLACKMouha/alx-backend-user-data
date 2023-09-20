#!/usr/bin/env python3
'''auth module'''

from flask import request
from typing import List, TypeVar


class Auth:
    '''API Authentication class manager'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''returns True if the path is not in the excluded paths list'''
        if not path or not excluded_paths:
            return True
        if not path.endswith('/'):
            path = path + '/'
        return not path in excluded_paths

    def authorization_header(self, request=None) -> str:
        '''authorization_header method'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''current_user method'''
        return None
