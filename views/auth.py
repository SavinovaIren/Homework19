import calendar
import datetime
import hashlib
from os import abort

import jwt

from flask import request
from flask_restx import Namespace, Resource
from constants import ALGO, SECRET
from models import User
from setup_db import db

auth_ns = Namespace("auth")


"""def generate_tokens(user_obj):
    data = {
        "username": user_obj.get('username'),
        "role": user_obj.get('role')
    }
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, SECRET, algorithm=ALGO)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

    return {"access_token": access_token, "refresh_token": refresh_token}"""

def get_hash(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)

        if None in [password, username]:
            abort(400)

        user = db.session.query(User).filter(User.username == username)

        if user is None:
            return {"error": "Такого пользователя нет"}, 401

        hash_hidest = get_hash(password)

        if hash_hidest != user.password:
            return {"error": "Неверный пароль"}, 401

        data = {"username": user.username,
                "password": user.password}

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201

