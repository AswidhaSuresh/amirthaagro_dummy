# app/extensions.py
# ------------------------------------------------------------
# Central extension instances for DB, serialization, etc.
# ------------------------------------------------------------

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Database instance
db = SQLAlchemy()

# Marshmallow for serialization
ma = Marshmallow()
