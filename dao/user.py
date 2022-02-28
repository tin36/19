from marshmallow import fields, Schema

from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_filter(self, filter_dict):
        return self.session.query(User).filter_by(**filter_dict).all()

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def create(self, data_in):
        obj = User(**data_in)
        self.session.add(obj)
        self.session.commit()
        return obj

    def update(self, data_in):
        obj = self.get_one(data_in.get('id'))
        if obj:
            if data_in.get('username'):
                obj.username = data_in.get('username')
            if data_in.get('password'):
                obj.password = data_in.get('password')
            if data_in.get('role'):
                obj.role = data_in.get('role')
            self.session.add(obj)
            self.session.commit()
            return obj

    def delete(self, uid):
        obj = self.get_one(uid)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return obj
        return None

