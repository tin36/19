import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import request, abort

from const import PWD_HASH_SALT, PWD_HASH_ITERATIONS, JWT_SECRET, JWT_ALGORETHM
from implemented import user_service

def auth_check():
    if 'Authorization' not in request.headers:
        return False
    token = request.headers['Authorization'].split('Bearer '[-1])
    return jwt_decode(token)

def jwt_decode(token):
    try:
        decode_jwt = jwt.decode(token, JWT_SECRET, JWT_ALGORETHM)
    except:
        return False
    else:
        return decode_jwt

def auth_required(func):
    def wrapper(*args, **kwargs):
        if auth_check():
            return func(*args, **kwargs)
        abort(401, '')
    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        decoded_jwt = auth_check()
        if decoded_jwt:
            role = decoded_jwt.get('role')
            if role == 'admin':
                return func(*args, **kwargs)
        abort(401, '')
    return wrapper


def make_user_password_hash(password):
    return base64.b64encode(hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    ))


def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data['exp'] = calendar.timegm(min30.timetuple())
    acces_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORETHM)
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data['exp'] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORETHM)
    return {'acces_token': acces_token, 'refresh_token': refresh_token}


def compare_passwords(password_hash, other_password):
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        hashlib.pbkdf2_hmac(
            'sha256', other_password.encode('utf-8'), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
    )


def login_user(req_json):
    user_name = req_json.get('username')
    user_pass = req_json.get('password')
    if user_name and user_pass:
        user = user_service.get_filter({'username': user_name})
        if user:
            pass_hashed = user[0].password
            req_json['role'] = user[0].role
            if compare_passwords(pass_hashed, user_pass):
                return generate_token(req_json)


def refresh_user_token(req_json):
    refresh_token = req_json.get('refresh_token')
    data = jwt.decode(refresh_token)
    if data:
        tokens = generate_token(data)
        return tokens
    return False
