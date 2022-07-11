from flask import request
from flask_restx import Resource, Namespace

from service.decorators import auth_required, admin_required
from models import Genre, GenreSchema
from setup_db import db

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @admin_required
    def get(self):
        rs = db.session.query(Genre).all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @auth_required
    def post(self):
        req_quest = request.json
        new_genre = Genre(**req_quest)
        with db.session.begin():
            db.session.add(new_genre)
        return f"Добавлена новая запись", 201


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @admin_required
    def get(self, rid):
        r = db.session.query(Genre).get(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @auth_required
    def put(self, rid):
        r = db.session.query(Genre).get(rid)
        req_quest = request.json
        r.name = req_quest.get("name")
        db.session.add(r)
        db.session.commit()
        return f"Запись с id {r.id} изменена",204

    @auth_required
    def delete(self, rid):
        r = db.session.query(Genre).get(rid)
        db.session.delete(r)
        db.session.commit()
        return f"Запись с id {r.id} удалена",204
