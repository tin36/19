from flask import request
from flask_restx import Resource, Namespace, reqparse

from dao.model.movie import MovieSchema
from implemented import movie_service
from service.auth import auth_required

movie_ns = Namespace('movies')
movie_schema = MovieSchema
movies_schema = MovieSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument('director_id', type=int)
parser.add_argument('genre_id', type=int)
parser.add_argument('year_id', type=int)

@movie_ns.route('/')
class MovieView(Resource):
    @movie_ns.expect(parser)
    @auth_required
    def get(self):
        req_args = parser.parse_args()
        if any(req_args.values()):
            all_movies = movie_service.get_filter(req_args)
        else:
            all_movies = movie_service.get_all()
        if all_movies:
            return movies_schema.dump(all_movies), 200
        return '', 404

    @auth_required
    def post(self):
        req_json = request.json
        new_movie = movie_service.create(req_json)
        return '', 201

@movie_ns.route('/')
class MovieView(Resource):
    @auth_required
    def get(self, uid: int):
        movie = movie_service.get_one(uid)
        if movie:
            return movies_schema.dump(movie), 200
        return '', 404