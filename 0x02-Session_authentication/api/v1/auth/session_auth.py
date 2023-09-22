#!/usr/bin/env python3
'''session_auth module'''

from api.v1.auth.auth import Auth
import uuid
from models.user import User
from flask import request, jsonify
import os


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Returns a User ID based on the session_id'''
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        '''Retrieves the User object based on a cookie value'''
        session_id_from_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id_from_cookie)
        return User.get(user_id) if User.get(user_id) else None


from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    '''Returns a User instance based on the email and password provided by the
    form request.
    '''
    user_email = request.form.get('email', None)
    if not user_email:
        return jsonify({"error": "email missing"}), 400

    user_pwd = request.form.get('password', None)
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400

    user_objs = User.search({'email': user_email})
    if user_objs:
        user_obj = user_objs[0]
        if not User.is_valid_password(user_obj, user_pwd):
            return jsonify({"error": "wrong password"}), 401
        if os.getenv('AUTH_TYPE', None) == 'session_auth':
            from api.v1.app import auth
            session_id = auth.create_session(user_obj.id)
            resp = jsonify(user_obj.to_json())
            resp.set_cookie(
                os.getenv('SESSION_NAME', '_my_session'),
                session_id)
            return resp
    return jsonify({"error": "no user found for this email"}), 404
