# app/schemas/user_schema.py
# ------------------------------------------------------------
# Marshmallow schemas for user-related data validation
# ------------------------------------------------------------

from marshmallow import Schema, fields, validate
from app.extensions import ma
from app.models.user import User


class CreateUserSchema(Schema):
    """
    Schema for admin to create a new user (admin or client).

    Fields:
        email: User's email address.
        role: Must be either 'admin' or 'client'.

    Author: Siva
    """
    email = fields.Email(required=True)
    role = fields.String(required=True, validate=validate.OneOf(["admin", "client"]))


class LoginSchema(Schema):
    """
    Schema for login using email and password.

    Fields:
        email: Registered user email.
        password: Secret password string.

    Author: Siva
    """
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class UserResponseSchema(Schema):
    """
    Schema for responding with user details (safe for public use).

    Fields:
        id: UUID of the user.
        email: User email.
        role: Role (admin or client).
        is_active: Whether the user is active.
        created_at: Timestamp.

    Author: Siva
    """
    id = fields.UUID()
    email = fields.Email()
    role = fields.String()
    is_active = fields.Boolean()
    created_at = fields.DateTime()


class UserModelSchema(ma.SQLAlchemySchema):
    """
    Full Marshmallow SQLAlchemy schema for internal DB operations.

    Author: Siva
    """
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field()
    email = ma.auto_field()
    role = ma.auto_field()
    is_active = ma.auto_field()
    created_at = ma.auto_field()
