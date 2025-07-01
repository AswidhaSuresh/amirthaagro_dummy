# app/schemas/client_schema.py
# ------------------------------------------------------------
# Marshmallow schemas for client-related data validation
# ------------------------------------------------------------

from marshmallow import Schema, fields, validate
from app.extensions import ma
from app.models.client import Client


class CreateClientSchema(Schema):
    """
    Schema for creating a new client.

    Fields:
        email: Client's email address.
        party_id: Unique ID assigned to the client/party.
        mobile_number: Optional mobile number.

    Author: Siva
    """
    email = fields.Email(required=True)
    party_id = fields.String(required=True, validate=validate.Length(min=3))
    mobile_number = fields.String(required=False, validate=validate.Length(equal=10))


class ClientResponseSchema(Schema):
    """
    Schema for responding with client details (safe for exposure).

    Fields:
        id: UUID of the client.
        user_id: UUID of the user linked to this client.
        party_id: Client's assigned party ID.
        party_name: Client's assigned party name.
        mobile_number: Contact number.
        password_set: Boolean indicating whether password is set.
        created_at: Timestamp of creation.
        status: Status of client account.

    Author: Siva
    """
    id = fields.UUID()
    party_id = fields.String()
    party_name = fields.String()
    mobile_number = fields.String()
    password_set = fields.Boolean()
    created_at = fields.DateTime()
    email = fields.Email(attribute="user.email")  # Nested attribute
    status = fields.Method("get_status", dump_only=True)  # 🔥 New field

    def get_status(self, obj):
        return "Active" if obj.user and obj.user.is_active else "Inactive"


class ClientLoginSchema(Schema):
    """
    Schema for client login via party_id and password.

    Fields:
        party_id: Unique party identifier.
        password: Secret password string.

    Author: Siva
    """
    party_id = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class UpdateClientSchema(Schema):
    """
    Schema to allow updating mobile number or email.

    Fields:
        email: Updated email (optional).
        mobile_number: Updated mobile number (optional).

    Author: Siva
    """
    email = fields.Email(required=False)
    mobile_number = fields.String(required=False, validate=validate.Length(equal=10))


class ClientModelSchema(ma.SQLAlchemySchema):
    """
    Full marshmallow model schema for loading/saving client model from DB.
    Utilizes SQLAlchemy integration with Marshmallow.

    Author: Siva
    """
    class Meta:
        model = Client
        load_instance = True

    id = ma.auto_field()
    user_id = ma.auto_field()
    party_id = ma.auto_field()
    password_set = ma.auto_field()
    mobile_number = ma.auto_field()
    created_at = ma.auto_field()

    # ✅ Added field to expose user's email (joined via relationship)
    email = fields.Email(attribute="user.email")
