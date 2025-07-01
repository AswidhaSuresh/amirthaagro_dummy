# app/schemas/admin_schema.py
# ------------------------------------------------------------
# Marshmallow schemas for admin-related data validation
# ------------------------------------------------------------

from marshmallow import Schema, fields, validate
from app.extensions import ma
from app.models.admin import Admin


class CreateAdminSchema(Schema):
    """
    Schema for creating a new admin.

    Fields:
        email: Admin email address.
        admin_id: Unique admin ID (e.g., AMRTH1001).
        admin_name: Full name of the admin.
        mobile_number: 10-digit mobile number.

    Author: Siva
    """
    email = fields.Email(required=True)
    admin_id = fields.String(required=True, validate=validate.Length(min=3))
    admin_name = fields.String(required=True, validate=validate.Length(min=3))
    mobile_number = fields.String(
        required=True,
        validate=validate.Regexp(r"^[6-9]\d{9}$", error="Enter a valid 10-digit Indian mobile number")
    )


class UpdateAdminSchema(Schema):
    """
    Schema for updating admin details.

    Fields:
        admin_name: Updated name (optional).
        mobile_number: Updated mobile number (optional).
        email: Updated email (optional).

    Author: Siva
    """
    admin_name = fields.String(required=False, validate=validate.Length(min=3))
    mobile_number = fields.String(
        required=False,
        validate=validate.Regexp(r"^[6-9]\d{9}$", error="Enter a valid 10-digit Indian mobile number")
    )
    email = fields.Email(required=False)


class AdminResponseSchema(Schema):
    """
    Schema for responding with admin details.

    Fields:
        id: UUID of the admin.
        admin_id: Admin unique ID.
        admin_name: Full name.
        mobile_number: Contact number.
        created_at: Timestamp.
        email: From linked user record.
        status: Status of admin account.

    Author: Siva
    """
    id = fields.UUID()
    admin_id = fields.String()
    admin_name = fields.String()
    mobile_number = fields.String()
    created_at = fields.DateTime()
    email = fields.Email(attribute="user.email")  # ✅ Linked via relationship
    status = fields.Method("get_status", dump_only=True)  # 🔥 New field

    def get_status(self, obj):
        return "Active" if obj.user and obj.user.is_active else "Inactive"

class AdminModelSchema(ma.SQLAlchemySchema):
    """
    Full Marshmallow schema for internal DB interactions.

    Author: Siva
    """
    class Meta:
        model = Admin
        load_instance = True

    id = ma.auto_field()
    user_id = ma.auto_field()
    admin_id = ma.auto_field()
    admin_name = ma.auto_field()
    mobile_number = ma.auto_field()
    created_at = ma.auto_field()
    email = fields.Email(attribute="user.email")
