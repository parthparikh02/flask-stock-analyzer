from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import BaseModel
from flask_jwt_extended import create_access_token
from datetime import timedelta
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=True)

    def get_id(self):
        return self.id

    def set_password(self, password: str) -> None:
        """Set password with hashing."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def get_jwt_identity(self):
        """Return the identity of the user for JWT."""
        return self.id

    @staticmethod
    def generate_token(user: 'User') -> str:
        """Generate a JWT for a user."""
        expires = timedelta(hours=12)
        return create_access_token(identity=user.id, expires_delta=expires)

    def __repr__(self) -> str:
        return f"<User {self.email}>"
