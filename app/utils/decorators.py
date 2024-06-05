from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_current_user


def is_user_admin(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        user = get_current_user()
        if all(not _ for _ in user.roles if _.slug == "admin"):
            return (
                jsonify({"message": "You are not allowed", "error": "forbidden"}),
                403
            )
        return func(*args, **kwargs)
    return wrapped
