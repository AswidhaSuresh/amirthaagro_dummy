# app/utils/jwt_utils.py
# ------------------------------------------------------------
# JWT utility functions: generate, decode, and support token generation
# ------------------------------------------------------------

import jwt
from datetime import datetime, timedelta
from jwt import ExpiredSignatureError, InvalidTokenError
from app.config.config_loader import config_loader

# Load JWT config
JWT_SECRET = config_loader.config["jwt"]["secret"]
JWT_ALGORITHM = config_loader.config["jwt"].get("algorithm", "HS256")


def decode_jwt(token: str) -> dict:
    """
    Decode any token manually (e.g. in refresh endpoint)
    """
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def generate_password_reset_token(user_id: str, expires_minutes: int = 30) -> str:
    """
    Generate a short-lived token for password reset emails
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_password_reset_token(token: str) -> str | None:
    """
    Verify the password reset token manually
    """
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded.get("user_id")
    except (ExpiredSignatureError, InvalidTokenError):
        return None
