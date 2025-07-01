# app/models/user.py
# ------------------------------------------------------------
# SQLAlchemy model for the users table
# ------------------------------------------------------------

from app.extensions import db
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)  # 'admin' or 'client'
    is_active = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship("Client", back_populates="user", uselist=False)
    admin = db.relationship("Admin", back_populates="user", uselist=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)