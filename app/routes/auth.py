from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User
from app.models.role import Role
from app.models.token_blocklist import TokenBlockList
import datetime

bp = Blueprint('auth', __name__)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = db.session.query(User).filter(User.email == data.get("email")).first()
    if email is None:
        password_hash = generate_password_hash(
            data.get("password"), method="pbkdf2:sha256", salt_length=8
        )
        user = User(
            name=data.get("name"), email=data.get("email"), password=password_hash
        )
        default_role = db.session.query(Role).filter(Role.slug == "user").first()
        if default_role:
            user.roles.append(default_role)
        else:
            return jsonify({"error": "Default role not found"}), 500

        db.session.add(user)
        db.session.commit()
        return jsonify({"Success": "User registered successfully!"})
    else:
        return jsonify({"error": "Email already taken"})


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = db.session.query(User).filter(User.email == email).first()

    if user and check_password_hash(user.password, password):
        # Pass a JSON serializable identity, such as user.id or user.email
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    data = request.get_json()
    user = db.get_or_404(entity=User, ident=current_user.id)
    if user and check_password_hash(user.password, data.get("current_password")):
        password_hash = generate_password_hash(
            data.get("new_password"), method="pbkdf2:sha256", salt_length=8
        )
        user.password = password_hash
        db.session.commit()
        return jsonify({"Success": "Password updated successfully!"})
    else:
        return jsonify({"error": "Invalid credentials"})


@bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.datetime.now(datetime.timezone.utc)
    new_blocked_token = TokenBlockList(
        jti=jti,
        created_at=now,
    )
    db.session.add(new_blocked_token)
    db.session.commit()
    return jsonify({"Success": "Logged out successfully!"}), 200


@bp.route("/who-am-i", methods=["GET"])
@jwt_required()
def who_am_i():
    user_details = {
        "current_user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "roles": [role.name for role in current_user.roles]
        }
    }
    return jsonify(user_details)
