from flask import jsonify
from app.models.user import User
from app.extensions import jwt
from app.extensions import db
from app.models.token_blocklist import TokenBlockList


@jwt.user_identity_loader
def user_identity(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identify = jwt_data["sub"]
    return User.query.filter_by(id=identify).one_or_none()


@jwt.expired_token_loader
def expired_token_callback(_jwt_header, jwt_data):
    return jsonify({"message": "Token has expired", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def missing_token_callback(error):
    return jsonify({"message": "Request doesn't contain valid token", "error": "authorization_required"}), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "Token has been revoked", "error": "token_revoked"}), 401


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlockList).filter_by(jti=jti).first()
    return token is not None
