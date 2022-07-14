from flask import Flask
from flask_restx import Api

from config import Config
from models import User
from setup_db import db
from views.auth import auth_ns, get_hash
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(application):
    db.init_app(application)
    api = Api(application)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)



app_ = create_app(Config())
app_.debug = True

if __name__ == '__main__':
    app_.run(host="localhost", port=10001, debug=True)
