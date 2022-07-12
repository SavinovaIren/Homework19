import base64
import calendar
import datetime
import hashlib
import hmac

import jwt

from flask import request, abort
from flask_restx import Namespace, Resource
from constants import SECRET
from models import User
from setup_db import db

auth_ns = Namespace("auth")


def get_hash(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()



def generate_token(username, password, is_fresh=False):
    if (password or username) is None:
        abort(400)

    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return {"error": "Такого пользователя нет"}, 401

    hash_hidest = get_hash(password)

    if not is_fresh:
        if user.password != hash_hidest:
            return {"error": "Пароль неверный"}, 401
        else:
            data = {"username": user.username,
                    "password": user.password}

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm="HS256")

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm="HS256")

        return {"access_token": access_token, "refresh_token": refresh_token}

def approve_refresh_token(refresh_token):
    data = jwt.decode(jwt=refresh_token, key=SECRET, algorithms=['HS256'])
    username = data.get("username")
    return generate_token(username, None,is_fresh=True)


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)

        tokens = generate_token(username, password)
        return tokens, 201

    def put(self):
        data = request.json
        token = data.get("refresh_token")
        tokens = approve_refresh_token(token)
        return tokens

