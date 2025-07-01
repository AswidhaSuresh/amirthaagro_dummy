# app/models/password_reset.py
# ------------------------------------------------------------
# SQLAlchemy model for the password_resets table
# ------------------------------------------------------------

from app.extensions import db
import uuid
from datetime import datetime

class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.Uuid, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = db.Column(db.String, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)