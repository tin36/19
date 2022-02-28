from flask import request
from flask_restx import Resource, Namespace, abort

from service.auth import login_user, refresh_user_token

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        if not request.json:
            abort(400, '')
        tokens = login_user(request.json)
        if tokens:
            return tokens, 200
        abort(401, '')

    def put(self):
        if not request.json:
            abort(400, '')
        tokens = refresh_user_token(request.json)
        if tokens:
            return tokens, 200
        abort(401, '')
