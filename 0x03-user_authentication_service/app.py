#!/usr/bin/env python3
'''Flask app'''

from flask import Flask, jsonify, request, abort, url_for, redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def root() -> dict:
    """ GET /
    Returns {'message': 'bienvenue'}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    '''User registeration endpoint'''
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    try:
        AUTH.register_user(
            email=email, password=password)
        return jsonify({'email': email, 'message': 'user created'}), 200
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    '''Login'''
    email = request.form.get('email', None)
    password = password = request.form.get('password', None)
    if not AUTH.valid_login(email=email, password=password):
        abort(401)
    session_id = AUTH.create_session(email=email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie('session_id', session_id)
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    '''Logout'''
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('root'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    '''Finding a user based on the session_id'''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
