from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.pokemon import Pokemon
from app.schemas.pokemon_schema import PokemonSchema
from app.utils.helpers import get_pokemon_data
import requests

bp = Blueprint('pokemon', __name__)

POKE_API = "https://pokeapi.co/api/v2/pokemon"


@bp.route("/get-all-pokemon")
def get_all_pokemon():
    pokemon_data = Pokemon.query.all()
    schema = PokemonSchema(many=True)
    return {"results": schema.dump(pokemon_data)}


@bp.route("/pokemon/<int:pokemon_id>")
def get_pokemon(pokemon_id):
    pokemon_data = Pokemon.query.get(pokemon_id)
    schema = PokemonSchema()
    return {"results": schema.dump(pokemon_data)}


@bp.route("/search", methods=["GET"])
@jwt_required()
def search():
    pokemon_name = request.args.get("pokemon_name", None)

    try:
        result = requests.get(f"{POKE_API}/{pokemon_name.lower()}?limit=100&offset=0")
        data = result.json()
        poke_data = get_pokemon_data(data)

    except requests.exceptions.RequestException:
        return jsonify({"error": f"There is no pokemon named {pokemon_name}"}), 400

    return jsonify(poke_data)
