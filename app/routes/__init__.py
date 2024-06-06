from flask import Flask
from app.routes import auth, pokemon, admin


def register_routes(app: Flask):
    app.register_blueprint(auth.bp)
    app.register_blueprint(pokemon.bp)
    app.register_blueprint(admin.bp)
