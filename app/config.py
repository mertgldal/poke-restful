import secrets


class Config:
    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = "sqlite:///pokedex.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
