from app.extensions import ma
from app.models.pokemon import Pokemon


class PokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pokemon
