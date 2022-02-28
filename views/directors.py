from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from service.auth import auth_required

director_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorView(Resource):
    @auth_required
    def get(self):
        all_directors = director_service.get_all()
        return directors_schema.dump(all_directors), 200

    @auth_required
    def post(self):
        req_json = request.json
        new_director = director_service.create(req_json)
        return '', 201

@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    @auth_required
    def get(self, uid: int):
        director = director_service.get_one(uid)
        if director:
            return director_schema.dump(director)
        return '', 404

    @auth_required
    def put(self, uid: int):
        req_json = request.json
        if not req_json.get('id'):
            req_json['id'] = uid
        if director_service.update(req_json):
            return'', 201

    @auth_required
    def delete(self, uid: int):
        if director_service.delete(uid):
            return '', 204
        return '', 404