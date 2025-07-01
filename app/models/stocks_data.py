# app/models/stocks_data.py

from app.extensions import db
import uuid
from datetime import datetime

class StocksData(db.Model):
    __tablename__ = 'stocks_data'

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)

    # Foreign key to clients
    party_id = db.Column(
        db.String,
        db.ForeignKey('clients.party_id', ondelete='CASCADE'),
        nullable=False
    )

    # ✅ Add this to fix the error
    party_name = db.Column(db.String, nullable=False)

    bank = db.Column(db.String, nullable=True)
    lot_no = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=True)
    mark = db.Column(db.String, nullable=True)
    lorry = db.Column(db.String, nullable=True)
    product = db.Column(db.String, nullable=False)
    packing = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    weight_kgs = db.Column(db.Float, nullable=True)
    chamber = db.Column(db.String, nullable=True)
    floor = db.Column(db.String, nullable=True)
    bayee = db.Column(db.String, nullable=True)

    uploaded_on = db.Column(db.DateTime, default=datetime.utcnow)

    # FK to users
    uploaded_by = db.Column(
        db.Uuid,
        db.ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True
    )
