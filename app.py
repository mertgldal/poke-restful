from flask import Flask, request, abort, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import requests
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)

POKE_API = 'https://pokeapi.co/api/v2/pokemon'

jwt = JWTManager(app)
ma = Marshmallow(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokedex.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Configure Tables
class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = relationship("User", back_populates="pokemon")
    name = db.Column(db.String, nullable=False)
    abilities = db.Column(db.String, nullable=False)
    types = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable=False)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    pokemon = relationship('Pokemon', back_populates='creator')


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['id']


class PokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pokemon


with app.app_context():
    db.create_all()


def is_user_admin(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.id == 2:
            return func(*args, **kwargs)
        return abort(403)

    return wrapped


def is_user_authenticated(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            return jsonify({'error': f'You have already logged in! You can not access the {func.__name__} page!'})
        return func(*args, **kwargs)

    return wrapped


def get_pokemon_data(data):
    pokemon_id = data.get("pokemon_id", None)
    pokemon_name = data.get("name", None)
    ability_list = [ability["ability"]["name"].title() for ability in data["abilities"]]
    type_list = [poke_type["type"]["name"].title() for poke_type in data["types"]]
    poke_data_dict = {
        "result":
            {
                "id": pokemon_id,
                "name": pokemon_name,
                "abilities": ability_list,
                "types": type_list,
                "poke_img": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
            }
    }
    return poke_data_dict


@jwt.user_identity_loader
def user_identity(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identify = jwt_data['sub']
    return User.query.filter_by(id=identify).one_or_none()


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to Pokemon API!'})


@app.route('/who-am-i', methods=["GET"])
@jwt_required()
def who_am_i():
    user_details = {
        "current_user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email
        }
    }
    return jsonify(user_details)


@app.route('/get-all-pokemon')
def get_all_pokemon():
    pokemon_data = Pokemon.query.all()
    schema = PokemonSchema(many=True)
    return {"results": schema.dump(pokemon_data)}


@app.route('/get-all-users')
@jwt_required()
@is_user_admin
def get_all_users():
    user_data = User.query.all()
    schema = UserSchema(many=True)
    return {"results": schema.dump(user_data)}


@app.route('/pokemon/<int:pokemon_id>')
def get_pokemon(pokemon_id):
    pokemon_data = Pokemon.query.get(pokemon_id)
    schema = PokemonSchema()
    return {"results": schema.dump(pokemon_data)}


@app.route('/register', methods=['POST'])
# @is_user_authenticated
def register():
    data = request.get_json()
    email = db.session.query(User).filter(User.email == data.get('email')).first()
    if email is None:
        password_hash = generate_password_hash(data.get('password'), method='pbkdf2:sha256', salt_length=8)
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            password=password_hash
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'Success': 'User registered successfully!'})
    else:
        return jsonify({'error': 'Email already taken'})


@app.route('/login', methods=['POST'])
# @is_user_authenticated
def login():
    data = request.get_json()
    user = db.session.query(User).filter(User.email == data.get('email')).first()
    if user and check_password_hash(user.password, data.get('password')):
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)
    else:
        return jsonify({'error': 'Invalid credentials'})


@app.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    user = db.get_or_404(entity=User, ident=current_user.id)
    if user and check_password_hash(user.password, data.get('current_password')):
        password_hash = generate_password_hash(data.get('new_password'), method='pbkdf2:sha256', salt_length=8)
        user.password = password_hash
        db.session.commit()
        return jsonify({'Success': 'Password updated successfully!'})
    else:
        return jsonify({'error': 'Invalid credentials'})


#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('home'))
#
#
@app.route('/search', methods=['GET'])
@jwt_required()
def search():
    pokemon_name = request.args.get("pokemon_name", None)

    try:
        result = requests.get(f'{POKE_API}/{pokemon_name.lower()}?limit=100&offset=0')
        data = result.json()
        poke_data = get_pokemon_data(data)

    except requests.exceptions.RequestException:
        return jsonify({"error": f"There is no pokemon named {pokemon_name}"}), 400

    return jsonify(poke_data)


@app.route('/add/<string:pokemon_name>', methods=['POST'])
@jwt_required()
@is_user_admin
def add(pokemon_name):
    result = requests.get(f'{POKE_API}/{pokemon_name.lower()}?limit=100&offset=0')
    data = result.json()
    poke_data = get_pokemon_data(data)
    print(poke_data)
    print(poke_data['result']['name'], ", ".join(poke_data['result']['abilities']),
          ", ".join(poke_data['result']['types']), poke_data['result']['poke_img'])
    print(current_user.name)
    pokemon = Pokemon(
        name=poke_data['result']['name'],
        creator=current_user,
        abilities=", ".join(poke_data['result']['abilities']),
        rating=0,
        types=", ".join(poke_data['result']['types']),
        image=poke_data['result']['poke_img'],
    )

    db.session.add(pokemon)
    db.session.commit()

    return jsonify({'Success': 'Pokemon added successfully!'})


@app.route('/edit-pokemon/<int:pokemon_id>', methods=["POST"])
@jwt_required()
@is_user_admin
def edit(pokemon_id):
    db.session.query(Pokemon).filter(Pokemon.id == pokemon_id).update(
        {
            'rating': float(request.args.get('rating', 0.0))
        }
    )
    db.session.commit()
    return jsonify({"Success": "Pokemon edited successfully!"})


@app.route('/delete/<int:pokemon_id>', methods=["GET", "POST"])
@jwt_required()
@is_user_admin
def delete(pokemon_id):
    pokemon = db.get_or_404(entity=Pokemon, ident=pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()
    return jsonify({"Success": "Pokemon deleted successfully!"})


if __name__ == "__main__":
    app.run(debug=False)
