#!/usr/bin/env python3
'''session_db_auth module'''
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from flask import request
import os


class SessionDBAuth(SessionExpAuth):
    '''Session Database Authentication class'''

    def create_session(self, user_id=None):
        '''Creates a new session and returns the UserSession session ID'''
        if not user_id:
            return None
        session_id = super().create_session(user_id)
        user_session_obj = UserSession(user_id=user_id,
                                       session_id=session_id)
        user_session_obj.save()
        return session_id

    def destroy_session(self, request=None):
        '''Deletes the user session'''
        if not request:
            return False
        session_id_from_cookie = request.cookies.get(
            os.getenv('SESSION_NAME', None), None)
        if not session_id_from_cookie:
            return False
        user_session_objs = UserSession.search(
            {'session_id': session_id_from_cookie})
        user_session_obj = user_session_objs[0]
        if not user_session_obj:
            return False
        del user_session_obj
        return True
