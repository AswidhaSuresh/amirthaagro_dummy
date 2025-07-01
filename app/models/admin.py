# app/models/admin.py
# ------------------------------------------------------------
# SQLAlchemy model for the admins table
# ------------------------------------------------------------
from app.extensions import db

class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Uuid, db.ForeignKey("users.id"), nullable=False)
    admin_id = db.Column(db.String(64), unique=True, nullable=False)
    admin_name = db.Column(db.String(128), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # 🔗 Relationship with User table
    user = db.relationship("User", back_populates="admin")
