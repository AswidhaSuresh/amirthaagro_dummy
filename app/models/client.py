# app/models/client.py
from app.extensions import db

class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Uuid, db.ForeignKey("users.id"), nullable=False)
    party_id = db.Column(db.String(64), unique=True, nullable=False)
    party_name = db.Column(db.String(128), nullable=False)
    mobile_number = db.Column(db.String(20))
    password_set = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # ✅ Fix here: use back_populates instead of backref
    user = db.relationship("User", back_populates="client")
