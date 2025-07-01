# ✅ UPDATED ADMIN ROUTES TO USE COOKIE-BASED JWT AUTH

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from app.extensions import db
from app.models.user import User
from app.models.client import Client
from app.schemas.user_schema import CreateUserSchema
from app.schemas.client_schema import ClientResponseSchema
from werkzeug.security import generate_password_hash
from app.config.logger_loader import app_logger
from app.utils.helpers import StockParseError, StockParser, helpers
from app.models.stocks_data import StocksData
from app.models.admin import Admin
from app.schemas.admin_schema import AdminResponseSchema


admin_bp = Blueprint("admin", __name__)


def is_admin():
    jwt_data = get_jwt()
    return jwt_data.get("role") == "admin"


@admin_bp.route("/create-admin", methods=["POST"])
@jwt_required(locations=["cookies"])
def create_admin():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    email = data.get("email")
    admin_id = data.get("admin_id")
    admin_name = data.get("admin_name")
    mobile_number = data.get("mobile_number")

    if not all([email, admin_id, admin_name, mobile_number]):
        return jsonify({"error": "All fields (email, admin_id, admin_name, mobile_number) are required."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    if Admin.query.filter_by(admin_id=admin_id).first():
        return jsonify({"error": "Admin ID already exists"}), 400

    # Create User (role = admin)
    user = User(email=email, role="admin")
    generated_password = helpers.generate_password(4)
    user.password_hash = generate_password_hash(generated_password)

    db.session.add(user)
    db.session.flush()  # To get user.id before admin insert

    # Create Admin record
    new_admin = Admin(
        user_id=user.id,
        admin_id=admin_id.strip().upper(),
        admin_name=admin_name.strip(),
        mobile_number=mobile_number
    )
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({
        "message": "Admin created successfully.",
        "email": email,
        "admin_id": admin_id,
        "password": generated_password
    }), 201


@admin_bp.route("/get-admin-info", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_admin_profile():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    if not user or user.role != "admin":
        return jsonify({"error": "Admin not found"}), 404

    admin = Admin.query.filter_by(user_id=user.id).first()
    if not admin:
        return jsonify({"error": "Admin profile not found"}), 404

    schema = AdminResponseSchema()
    return jsonify(schema.dump(admin)), 200


@admin_bp.route("/list-admins", methods=["GET"])
@jwt_required(locations=["cookies"])
def list_admins():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    admins = Admin.query.all()
    schema = AdminResponseSchema(many=True)
    return jsonify(schema.dump(admins)), 200


@admin_bp.route("/update-admin-profile", methods=["PATCH"])
@jwt_required(locations=["cookies"])
def update_admin_profile():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    admin = Admin.query.filter_by(user_id=user.id).first()
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email")
    admin_name = data.get("admin_name")
    mobile = data.get("mobile_number")

    # --- 🔐 Validate Email uniqueness ---
    if email and email != user.email:
        existing_email = User.query.filter(User.email == email, User.id != user.id).first()
        if existing_email:
            return jsonify({"error": "Email already in use"}), 400
        user.email = email

    # --- 🔐 Validate Admin Name uniqueness ---
    if admin_name and admin_name != admin.admin_name:
        existing_name = Admin.query.filter(Admin.admin_name == admin_name, Admin.id != admin.id).first()
        if existing_name:
            return jsonify({"error": "Admin name already in use"}), 400
        admin.admin_name = admin_name

    # --- 🔐 Validate Mobile Number uniqueness ---
    if mobile and mobile != admin.mobile_number:
        existing_mobile = Admin.query.filter(Admin.mobile_number == mobile, Admin.id != admin.id).first()
        if existing_mobile:
            return jsonify({"error": "Mobile number already in use"}), 400
        admin.mobile_number = mobile

    db.session.commit()
    return jsonify({"message": "Admin profile updated successfully."}), 200


@admin_bp.route("/update-admin-password", methods=["PATCH"])
@jwt_required(locations=["cookies"])
def update_admin_password():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    current_password = data.get("current_password")
    new_password = data.get("new_password")

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.check_password(current_password):
        return jsonify({"error": "Current password is incorrect"}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password updated successfully."}), 200


@admin_bp.route("/reset-admin-password/<string:admin_id>", methods=["POST"])
@jwt_required(locations=["cookies"])
def reset_admin_password(admin_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    admin = Admin.query.filter_by(admin_id=admin_id).first()
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    user = User.query.get(admin.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_password = helpers.generate_password(4)
    user.set_password(new_password)
    db.session.commit()

    return jsonify({
        "message": "Password reset successful.",
        "email": user.email,
        "password": new_password
    }), 200


@admin_bp.route("/deactivate-admin/<string:admin_id>", methods=["PATCH"])
@jwt_required(locations=["cookies"])
def deactivate_admin(admin_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    admin = Admin.query.filter_by(admin_id=admin_id).first()
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    user = User.query.get(admin.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_active = False
    db.session.commit()

    return jsonify({"message": "Admin deactivated successfully"}), 200


@admin_bp.route("/reactivate-admin/<string:admin_id>", methods=["PATCH"])
@jwt_required(locations=["cookies"])
def reactivate_admin(admin_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    admin = Admin.query.filter_by(admin_id=admin_id).first()
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    user = User.query.get(admin.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_active = True
    db.session.commit()

    return jsonify({"message": "Admin reactivated successfully"}), 200


@admin_bp.route("/create-client", methods=["POST"])
@jwt_required(locations=["cookies"])
def create_client():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()

    user_schema = CreateUserSchema()
    errors = user_schema.validate({
        "email": data.get("email"),
        "role": "client"
    })
    if errors:
        return jsonify({"errors": errors}), 400

    # Validation
    if not data.get("party_id"):
        return jsonify({"error": "party_id is required"}), 400
    if not data.get("party_name"):
        return jsonify({"error": "party_name is required"}), 400

    if Client.query.filter_by(party_id=data["party_id"]).first():
        return jsonify({"error": "party_id already exists"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    # Create user
    new_user = User(email=data["email"], role="client")
    new_password = helpers.generate_password(4)
    new_user.password_hash = generate_password_hash(new_password)

    db.session.add(new_user)
    db.session.flush()

    # Create client
    new_client = Client(
        user_id=new_user.id,
        party_id=data["party_id"],
        party_name=data["party_name"],  # ✅ Add to DB
        mobile_number=data.get("mobile_number"),
        password_set=True
    )
    db.session.add(new_client)
    db.session.commit()

    return jsonify({
        "message": "Client created and credentials sent via email.",
        "password": new_password  # ✅ Send password to frontend
    }), 201


@admin_bp.route("/list-clients", methods=["GET"])
@jwt_required(locations=["cookies"])
def list_clients():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    clients = Client.query.all()
    client_schema = ClientResponseSchema(many=True)
    return jsonify(client_schema.dump(clients)), 200


@admin_bp.route("/reset-client-password/<string:party_id>", methods=["POST"])
@jwt_required(locations=["cookies"])
def reset_client_password(party_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    # Get client and related user
    client = Client.query.filter_by(party_id=party_id).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    user = User.query.get(client.user_id)
    if not user:
        return jsonify({"error": "User associated with client not found"}), 404

    # Generate new password and update
    new_password = helpers.generate_password(4)
    user.password_hash = generate_password_hash(new_password)

    db.session.commit()

    # Respond with email and new password
    return jsonify({
        "email": user.email,
        "password": new_password
    }), 200


@admin_bp.route("/upload-stocks", methods=["POST"])
@jwt_required(locations=["cookies"])
def upload_stocks():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    if not uploaded_file.filename.endswith((".xlsx", ".xls")):
        return jsonify({"error": "Invalid file format. Only .xlsx or .xls allowed."}), 400

    try:
        parsed_data = StockParser.extract_stock_data(uploaded_file)
        print(parsed_data)
        if not parsed_data:
            return jsonify({"error": "No stock data found in file."}), 400

        uploaded_by = get_jwt_identity()
        print(uploaded_by)
        for record in parsed_data:
            party_name = record["party_name"]
            print("party_name", party_name)
            client = Client.query.filter_by(party_name=party_name).first()
            print(client)
            if not client:
                continue  # or collect for error reporting
            print("party_name", party_name)
            stock = StocksData(
                party_id=client.party_id,
                party_name=party_name,
                bank=record["bank"],
                lot_no=record["lot_no"],
                date=record["date"],
                mark=record["mark"],
                lorry=record["lorry"],
                product=record["product"],
                packing=record["packing"],
                quantity=record["quantity"],
                weight_kgs=record["weight_kgs"],
                chamber=record["chamber"],
                floor=record["floor"],
                bayee=record["bayee"],
                uploaded_by=uploaded_by
            )
            db.session.add(stock)

        db.session.commit()
        return jsonify({"message": "Stocks uploaded and saved successfully."}), 201

    except StockParseError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        app_logger.error(f"Stock upload error: {e}")
        return jsonify({"error": "Internal server error while processing stocks."}), 500


@admin_bp.route("/update-client/<string:party_id>", methods=["PATCH"])
@jwt_required(locations=["cookies"])
def update_client(party_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    client = Client.query.filter_by(party_id=party_id).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    user = User.query.get(client.user_id)
    if not user:
        return jsonify({"error": "Associated user not found"}), 404

    # Update fields if they exist in the payload
    party_name = data.get("party_name")
    email = data.get("email")
    mobile_number = data.get("mobile_number")

    if party_name:
        client.party_name = party_name
    if mobile_number:
        client.mobile_number = mobile_number
    if email:
        # Ensure email is unique
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"error": "Email already in use"}), 400
        user.email = email

    db.session.commit()

    return jsonify({"message": "Client updated successfully"}), 200


@admin_bp.route("/deactivate-client/<string:party_id>", methods=["PATCH"])
@jwt_required(locations=["cookies"])
def deactivate_client(party_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    client = Client.query.filter_by(party_id=party_id).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    user = User.query.get(client.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_active = False
    db.session.commit()

    return jsonify({"message": "Client deactivated successfully"}), 200


@admin_bp.route("/reactivate-client/<string:party_id>", methods=["PATCH"])
@jwt_required(locations=["cookies"])
def reactivate_client(party_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    client = Client.query.filter_by(party_id=party_id).first()
    if not client:
        return jsonify({"error": "Client not found"}), 404

    user = User.query.get(client.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.is_active = True
    db.session.commit()

    return jsonify({"message": "Client reactivated successfully"}), 200
