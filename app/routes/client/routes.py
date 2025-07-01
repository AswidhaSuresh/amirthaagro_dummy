from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.client import Client
from app.models.stocks_data import StocksData
from app.models.user import User

client_bp = Blueprint("client", __name__)

@client_bp.route("/ping", methods=["GET"])
def ping():
    return {"message": "Client service running"}


@client_bp.route("/stocks", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_client_stocks():
    identity = get_jwt_identity()
    user = User.query.get(identity)

    if not user or user.role != "client":
        return jsonify({"error": "Unauthorized"}), 403

    client = Client.query.filter_by(user_id=user.id).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    stocks = StocksData.query.filter_by(party_id=client.party_id).order_by(StocksData.uploaded_on.desc()).all()

    result = []
    for stock in stocks:
        result.append({
            "product": stock.product,
            "quantity": stock.quantity,
            "lot_no": stock.lot_no,
            "date": stock.date.isoformat() if stock.date else None,
            "packing": stock.packing,
            "weight_kgs": stock.weight_kgs,
            "bank": stock.bank,
            "mark": stock.mark,
            "lorry": stock.lorry,
            "chamber": stock.chamber,
            "floor": stock.floor,
            "bayee": stock.bayee,
            "uploaded_on": stock.uploaded_on.isoformat(),
        })

    return jsonify({"stocks": result}), 200
