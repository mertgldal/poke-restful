from app.extensions import db
from sqlalchemy.orm import relationship


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(36), nullable=False)
    slug = db.Column(db.String(36), unique=True, nullable=False)

    users = relationship("User", secondary="user_roles", back_populates="roles")
