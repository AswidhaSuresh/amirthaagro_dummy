# schemas/auth_schema.py
# ------------------------------------------------------------
# Marshmallow schemas for user authentication and validation
# ------------------------------------------------------------

from marshmallow import Schema, fields, validate, ValidationError


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=4))


class AdminRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=4))


class RegisterUserSchema(Schema):
    email = fields.Email(required=True)
    role = fields.Str(required=True, validate=validate.OneOf(["admin", "client"]))


class OTPVerificationSchema(Schema):
    client_id = fields.Str(required=True)
    otp = fields.Str(required=True, validate=validate.Length(equal=6))
