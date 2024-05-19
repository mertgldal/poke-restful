from flask import Flask, request, abort, jsonify
from flask_jwt_extended import get_jwt, create_access_token, jwt_required, JWTManager, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import Integer, String, ForeignKey, Float, Identity
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import requests
from dataclasses import dataclass
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
        exclude = ['id']


with app.app_context():
    db.create_all()


def is_user_admin(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.get_id() == "1":
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


@app.route('/get-all-pokemon')
def get_all_pokemon():
    pokemon_data = Pokemon.query.all()
    schema = PokemonSchema(many=True)
    return {"results": schema.dump(pokemon_data)}


@app.route('/get-all-users')
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
# @app.route('/search', methods=['GET', 'POST'])
# @login_required
# @is_user_admin
# def search():
#     form = SearchForm()
#     pokemon_id = request.args.get('pokemon_id', None)
#     if form.validate_on_submit():
#         pokemon_name = form.title.data
#         result = requests.get(f'{POKE_API}/{pokemon_name.lower()}?limit=100&offset=0')
#         data = result.json()
#         print(data["name"])
#         return render_template("pokemon_details.html", pokemon=data)
#     elif pokemon_id:
#         pokemon_name = request.args.get('pokemon_name', None)
#         ability = request.args.get('pokemon_abilities', None)
#         types = request.args.get('pokemon_types', None)
#         poke_img = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
#         pokemon = Pokemon(
#             id=pokemon_id,
#             name=pokemon_name,
#             creator=current_user,
#             abilities=ability,
#             rating=0,
#             types=types,
#             image=poke_img,
#         )
#         db.session.add(pokemon)
#         db.session.commit()
#         return redirect(url_for("edit", pokemon_id=pokemon_id))
#     else:
#         return render_template("search_page.html", form=form)
#
#
# @app.route('/edit-pokemon/<int:pokemon_id>', methods=["GET", "POST"])
# @login_required
# @is_user_admin
# def edit(pokemon_id):
#     edit_form = EditForm()
#     if edit_form.validate_on_submit():
#         db.session.query(Pokemon).filter(Pokemon.id == pokemon_id).update(
#             {
#                 'rating': edit_form.rating.data
#             }
#         )
#         db.session.commit()
#         return redirect(url_for('home'))
#     else:
#         return render_template("edit.html", form=edit_form)
#
#
# @app.route('/delete/<int:pokemon_id>', methods=["GET", "POST"])
# @login_required
# @is_user_admin
# def delete(pokemon_id):
#     pokemon = db.get_or_404(entity=Pokemon, ident=pokemon_id)
#     db.session.delete(pokemon)
#     db.session.commit()
#     return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
