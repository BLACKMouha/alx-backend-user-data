#!/usr/bin/env python3
'''session_auth module'''

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    '''New authentication mechanism for simulating Users Sessions'''

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''Creates a new Session ID for a user_id'''
        if not isinstance(user_id, str):
            return None
        session_id = uuid.uuid4().__str__()
        self.user_id_by_session_id[session_id] = user_id
        return session_id