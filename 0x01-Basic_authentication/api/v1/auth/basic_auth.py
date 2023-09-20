#!/usr/bin/env python3
'''basci_auth module'''

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    '''`Basic` Authentication class manager'''

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        '''Extracts the Base64 part of a Basic Authorization header
        '''
        if type(authorization_header) is str\
                and authorization_header.startswith('Basic '):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        '''Decodes the Base64 part of a Basic Authorization header
        '''
        if type(base64_authorization_header) is str:
            if base64_authorization_header.startswith('Basic '):
                b = self.extract_base64_authorization_header(
                    base64_authorization_header)
            else:
                b = base64_authorization_header
            try:
                return base64.b64decode(b).decode()
            except Exception as e:
                return None
        return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        '''Returns the user email and password from the Base64 decoded value'''
        if type(decoded_base64_authorization_header) is str\
                and ':' in decoded_base64_authorization_header:
            r = decoded_base64_authorization_header.split(':')
            return (r[0], r[1])
        return None
