from marshmallow import Schema, fields
from app.extensions import ma
from app.models.stocks_data import StocksData

class StocksDataSchema(Schema):
    """Schema for validating and serializing stock records."""

    id = fields.UUID(dump_only=True)

    party_id = fields.String(required=True)
    party_name = fields.String(required=True)

    bank = fields.String(allow_none=True)
    lot_no = fields.String(required=True)
    date = fields.Date(allow_none=True)
    mark = fields.String(allow_none=True)
    lorry = fields.String(allow_none=True)
    product = fields.String(required=True)
    packing = fields.Float(allow_none=True)
    quantity = fields.Integer(allow_none=True)
    weight_kgs = fields.Float(allow_none=True)
    chamber = fields.String(allow_none=True)
    floor = fields.String(allow_none=True)
    bayee = fields.String(allow_none=True)

    uploaded_on = fields.DateTime(dump_only=True)
    uploaded_by = fields.UUID(allow_none=True)


class StocksDataResponseSchema(Schema):
    """Schema for responding with a stock entry."""
    id = fields.UUID()
    party_id = fields.String()
    party_name = fields.String()
    bank = fields.String()
    lot_no = fields.String()
    date = fields.Date(allow_none=True)
    mark = fields.String()
    lorry = fields.String()
    product = fields.String()
    packing = fields.Float()
    quantity = fields.Integer()
    weight_kgs = fields.Float()
    chamber = fields.String()
    floor = fields.String()
    bayee = fields.String()
    uploaded_on = fields.DateTime()
    uploaded_by = fields.UUID(allow_none=True)


class StocksDataModelSchema(ma.SQLAlchemySchema):
    """
    SQLAlchemy-based Marshmallow schema for direct use with StocksData model.
    Suitable for automated serialization and deserialization.
    """
    class Meta:
        model = StocksData
        load_instance = True

    id = ma.auto_field()
    party_id = ma.auto_field()
    party_name = ma.auto_field()
    bank = ma.auto_field()
    lot_no = ma.auto_field()
    date = ma.auto_field()
    mark = ma.auto_field()
    lorry = ma.auto_field()
    product = ma.auto_field()
    packing = ma.auto_field()
    quantity = ma.auto_field()
    weight_kgs = ma.auto_field()
    chamber = ma.auto_field()
    floor = ma.auto_field()
    bayee = ma.auto_field()
    uploaded_on = ma.auto_field()
    uploaded_by = ma.auto_field()
