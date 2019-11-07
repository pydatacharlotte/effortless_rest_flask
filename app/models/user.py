"User Model"
# pylint: disable=no-member
from app import db
from sqlalchemy.sql import func

# A generic user model that might be used by an app powered by flask-praetorian
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default="true")
    created_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now()
    )

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @classmethod
    def lookup(cls, username: str):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, user_id: int):
        return cls.query.get(user_id)

    @property
    def identity(self):
        return self.user_id

    def is_valid(self):
        return self.is_active

    def __repr__(self):
        return f"<User {self.user_id} - {self.username}>"
