#!/usr/bin/env python3
'''basci_auth module'''

from api.v1.auth.auth import Auth


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
