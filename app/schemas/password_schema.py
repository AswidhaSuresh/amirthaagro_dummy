# app/schemas/password_schema.py
# ------------------------------------------------------------
# Password setup schema for first-time user onboarding
# ------------------------------------------------------------

from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class RequestPasswordSetupSchema(Schema):
    party_id = fields.String(required=True)


class PasswordSetupSchema(Schema):
    token = fields.String(required=True)
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters long.")
    )
    confirm_password = fields.String(required=True)

    @validates_schema
    def validate_password_match(self, data, **kwargs):
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError("Passwords do not match.", field_name="confirm_password")


class PasswordResetRequestSchema(Schema):
    email = fields.Email(required=True)