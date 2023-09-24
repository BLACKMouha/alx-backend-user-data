#!/usr/bin/env python3
'''Flask app'''

from flask import Flask, jsonify, request
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth, _hash_password

AUTH = Auth()

app = Flask(__name__)



@app.route('/', methods=['GET'], strict_slashes=False)
def root() -> dict:
    """ GET /
    Returns {'message': 'bienvenue'}
    """
    return jsonify({"message": "Bienvenue"})

d = {'a': 1, 'b': 2}
d.__contains__('a')

@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    '''User registeration endpoint'''
    if all(request.form.__contains__(k) for k in request.form):
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        print(email, password)
        try:
            user = AUTH.register_user(
                email=email, password=password)
            return jsonify({'email': email, 'message': 'user created'})
        except ValueError:
            return jsonify({'message': 'email already registered'})
    else:
        return jsonify({'message': 'missing email or password'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
