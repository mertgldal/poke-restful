from app.extensions import db
from sqlalchemy.orm import relationship


class Pokemon(db.Model):
    __tablename__ = "pokemon"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    creator = relationship("User", back_populates="pokemon")
    name = db.Column(db.String, nullable=False)
    abilities = db.Column(db.String, nullable=False)
    types = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable=False)
