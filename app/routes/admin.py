import requests
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.pokemon import Pokemon
from app.schemas.user_schema import UserSchema
from app.utils.decorators import is_user_admin
from app.utils.helpers import get_pokemon_data

bp = Blueprint('admin', __name__)

POKE_API = "https://pokeapi.co/api/v2/pokemon"


@bp.route("/")
def home():
    return jsonify({"message": "Welcome to the flask pokedex!"}), 200


@bp.route("/get-all-users")
@jwt_required()
@is_user_admin
def get_all_users():
    user_data = User.query.all()
    schema = UserSchema(many=True)
    return {"results": schema.dump(user_data)}


@bp.route("/add/<string:pokemon_name>", methods=["POST"])
@jwt_required()
@is_user_admin
def add(pokemon_name):
    result = requests.get(f"{POKE_API}/{pokemon_name.lower()}?limit=100&offset=0")
    data = result.json()
    poke_data = get_pokemon_data(data)
    pokemon = Pokemon(
        name=poke_data["result"]["name"],
        creator=current_user,
        abilities=", ".join(poke_data["result"]["abilities"]),
        rating=0,
        types=", ".join(poke_data["result"]["types"]),
        image=poke_data["result"]["poke_img"],
    )

    db.session.add(pokemon)
    db.session.commit()

    return jsonify({"Success": "Pokemon added successfully!"})


@bp.route("/edit-pokemon/<int:pokemon_id>", methods=["POST"])
@jwt_required()
@is_user_admin
def edit(pokemon_id):
    db.session.query(Pokemon).filter(Pokemon.id == pokemon_id).update(
        {"rating": float(request.args.get("rating", 0.0))}
    )
    db.session.commit()
    return jsonify({"Success": "Pokemon edited successfully!"})


@bp.route("/delete/<int:pokemon_id>", methods=["DELETE"])
@jwt_required()
@is_user_admin
def delete(pokemon_id):
    pokemon = db.get_or_404(entity=Pokemon, ident=pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()
    return jsonify({"Success": "Pokemon deleted successfully!"})
