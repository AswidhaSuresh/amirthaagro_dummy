# app/schemas/password_reset_schema.py
# ------------------------------------------------------------
# Marshmallow schemas for password reset flow
# ------------------------------------------------------------

from marshmallow import Schema, fields, validate
from app.extensions import ma
from app.models.password_reset import PasswordReset


class PasswordResetRequestSchema(Schema):
    """
    Schema for requesting a password reset link.

    Fields:
        email: Registered email of the user (client or admin).

    Author: Siva
    """
    email = fields.Email(required=True)


class PasswordResetVerifySchema(Schema):
    """
    Schema for verifying a reset token.

    Fields:
        token: Unique token sent to user email.

    Author: Siva
    """
    token = fields.String(required=True)


class PasswordUpdateSchema(Schema):
    """
    Schema to update password via token.

    Fields:
        token: Reset token received via email.
        new_password: New password to set.
        confirm_password: Confirmation of the new password.

    Author: Siva
    """
    token = fields.String(required=True)
    new_password = fields.String(required=True, validate=validate.Length(min=6))
    confirm_password = fields.String(required=True, validate=validate.Length(min=6))


class PasswordResetModelSchema(ma.SQLAlchemySchema):
    """
    Full model schema for working with password_resets table.

    Author: Siva
    """
    class Meta:
        model = PasswordReset
        load_instance = True

    id = ma.auto_field()
    user_id = ma.auto_field()
    token = ma.auto_field()
    expires_at = ma.auto_field()
    used = ma.auto_field()
    created_at = ma.auto_field()
