# ✅ FINAL COOKIE-BASED AUTH ROUTES

from flask import Blueprint, make_response, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt,
    jwt_required, get_jwt_identity,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)
from app.extensions import db
from app.models.user import User
from app.schemas.auth_schema import AdminRegisterSchema, LoginSchema
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from app.config.logger_loader import app_logger
from app.models.admin import Admin
from app.models.client import Client


auth_bp = Blueprint("auth", __name__)


def is_admin():
    jwt_data = get_jwt()
    return jwt_data.get("role") == "admin"


@auth_bp.route("/ping", methods=["GET"])
def ping():
    return {"message": "Auth service running"}


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login route that sets JWT access and refresh tokens as HttpOnly cookies.
    """
    try:
        data = request.get_json()
        LoginSchema().load(data)

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not user.is_active:
            return jsonify({"error": "Invalid credentials."}), 401

        if not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Incorrect password."}), 401

        identity = {"user_id": str(user.id), "role": user.role}
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role}
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            additional_claims={"role": user.role}
        )

        response = make_response(jsonify({
            "message": "Login successful",
            "role": user.role,
            "user_id": str(user.id)
        }))

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        app_logger.exception("Login error:")
        return jsonify({"error": "Internal server error."}), 500


@auth_bp.route("/validate", methods=["GET"])
@jwt_required(locations=["cookies"])
def validate():
    user_id = get_jwt_identity()       # This is a string now
    role = get_jwt().get("role")       # Comes from additional_claims

    return jsonify({
        "message": "Token valid",
        "user_id": user_id,
        "role": role
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True, locations=["cookies"])
def refresh_token():
    """
    Uses refresh token to issue new access & refresh tokens.
    """
    identity = get_jwt_identity()
    role = get_jwt().get("role")  # 👈 extract from old refresh token

    new_access_token = create_access_token(
        identity=identity,
        additional_claims={"role": role}
    )
    new_refresh_token = create_refresh_token(
        identity=identity,
        additional_claims={"role": role}
    )

    response = make_response(jsonify({
        "message": "Token refreshed successfully."
    }))
    set_access_cookies(response, new_access_token)
    set_refresh_cookies(response, new_refresh_token)

    response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Logs out the user by clearing JWT cookies.
    """
    response = make_response(jsonify({"message": "Logged out successfully."}))
    unset_jwt_cookies(response)

    response.headers["Access-Control-Allow-Origin"] = "http://localhost:8080"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@auth_bp.route("/register-admin", methods=["POST"])
def register_admin():
    """
    One-time setup to register an admin user.
    """
    try:
        data = request.get_json()
        schema = AdminRegisterSchema()
        errors = schema.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        email = data["email"]
        password = data["password"]

        existing = User.query.filter_by(email=email).first()
        if existing:
            return jsonify({"error": "Admin with this email already exists."}), 400

        new_user = User(email=email, role="admin")
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Admin registered successfully."}), 201

    except Exception as e:
        app_logger.exception("Admin registration error:")
        return jsonify({"error": "Internal server error."}), 500


@auth_bp.route("/current-user", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    role = "Admin" if is_admin() else "Client"
    name = None

    if role == "Admin":
        admin = Admin.query.filter_by(user_id=user.id).first()
        name = admin.admin_name if admin else "Admin"
    else:
        client = Client.query.filter_by(user_id=user.id).first()
        name = client.party_name if client else "Client"

    return jsonify({
        "name": name,
        "role": role,
    }), 200
