# app/routes/__init__.py
# ------------------------------------------------------------
# Blueprint registrar for routing modularity
# ------------------------------------------------------------

from flask import Flask
from .auth.routes import auth_bp
from .admin.routes import admin_bp
from .client.routes import client_bp


def register_blueprints(app: Flask):
    """
    Registers all blueprint modules to the Flask app.

    Args:
        app (Flask): The main Flask app instance
    """
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(client_bp, url_prefix='/api/client')
