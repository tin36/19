import base64
import hashlib

from const import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_all(self):
        return self.user_dao.get_all()

    def get_one(self, uid):
        return self.user_dao.get_one(uid)

    def get_filter(self, filter_dict):
        filter_dict_clear = {}
        for key, value in filter_dict.items():
            if value is not None:
                filter_dict_clear[key] = value
        return self.user_dao.get_filter(filter_dict_clear)

    def create(self, data_in):
        user_pass = data_in.get('password')
        if user_pass:
            data_in['password'] = get_hash(user_pass)
        return self.user_dao.create(data_in)

    def update(self, data_in):
        user_pass = data_in.get('password')
        if user_pass:
            data_in['password'] = get_hash(user_pass)
        return self.user_dao.update(data_in)

    def delete(self, uid):
        self.user_dao.delete(uid)


def get_hash(password):
    return base64.b64encode(hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS))
