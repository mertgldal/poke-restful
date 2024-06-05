from app.extensions import db
import datetime


class TokenBlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String, unique=True, index=True, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )
