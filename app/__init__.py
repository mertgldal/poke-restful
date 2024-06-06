from flask import Flask
from app.extensions import db, ma, jwt
from app.config import Config
from app.routes import register_routes
from app.models import User
import app.jwt_callbakcs


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)

    return app
