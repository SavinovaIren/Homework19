import hashlib

from flask import request
from flask_restx import Namespace, Resource

from models import User
from setup_db import db
from service.decorators import auth_required
from views.auth import get_hash

user_ns = Namespace("users")


@user_ns.route("/")
class UserView(Resource):
    @auth_required
    def post(self):
        req_json = request.json
        ent = User(**req_json)
        ent.password= get_hash(req_json['password'])
        db.session.add(ent)
        db.session.commit()
        return "Добавлен новый пользователь", 200
