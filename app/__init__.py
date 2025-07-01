from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config.config_loader import config_loader
from app.config.logger_loader import app_logger
from app.utils.helpers import helpers
from app.extensions import db, ma
from app.routes import register_blueprints

jwt = JWTManager()

def create_app():
    """
    Application factory function.
    Creates and configures the Flask application.
    
    Returns:
        Flask app instance
    """
    app = Flask(__name__)

    CORS(app, supports_credentials=True, origins=["http://localhost:8080"])
    
    # Load base config
    app.config.update(config_loader.config.get("flask", {}))

    # Set SQLAlchemy DB URI from env.json
    app.config["SQLALCHEMY_DATABASE_URI"] = config_loader.config["database"]["url"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True  # ✅ Automatically test connections before using them
    }
    # JWT Config (🔐 REQUIRED)
    app.config["JWT_SECRET_KEY"] = config_loader.config.get("jwt", {}).get("secret", "amirtha-agro-client-dashboard")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # 🔐 disables CSRF check
    
    # Access token expiry: Get minutes from config, convert to timedelta
    access_token_expiry_minutes = config_loader.config.get("jwt", {}).get("access_token_expiry_minutes", 60)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=access_token_expiry_minutes)

    # Refresh token expiry: Get days from config, convert to timedelta
    refresh_token_expiry_days = config_loader.config.get("jwt", {}).get("refresh_token_expiry_days", 7)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=refresh_token_expiry_days)
    
    app.config["JWT_COOKIE_SECURE"] = False         # For localhost only
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"       # Optional, helps cookie delivery

    # Log app initialization
    app_logger.info("🚀 Creating Flask App with loaded configuration...")

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Register routes/blueprints
    register_blueprints(app)

    # Log ready status
    app_logger.info("✅ Flask App Initialized Successfully.")
    return app
