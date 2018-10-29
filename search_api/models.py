from geoalchemy2 import Geometry
from search_api.extensions import db
from search_api.utilities.charge_id import encode_charge_id
from sqlalchemy.dialects.postgresql import JSONB
from llc_schema_dto import llc_schema
from search_api import config


class LocalLandCharge(db.Model):
    __tablename__ = 'local_land_charge'

    id = db.Column(db.BigInteger, primary_key=True)
    geometry = db.relationship('GeometryFeature', back_populates='local_land_charge', cascade="all, delete-orphan")
    type = db.Column(db.String, nullable=False)
    llc_item = db.Column(JSONB, nullable=False)
    cancelled = db.Column(db.Boolean, nullable=False)
    further_information_reference = db.Column(db.String, nullable=True)

    def __init__(self, id, geometry, type, llc_item, cancelled, further_information_reference):
        self.id = id
        self.geometry = geometry
        self.type = type
        self.llc_item = llc_item
        self.cancelled = cancelled
        self.further_information_reference = further_information_reference

    def to_dict(self):
        return {
            "id": self.id,
            "display_id": encode_charge_id(self.id),
            "geometry": self.llc_item['geometry'],
            "type": self.type,
            "item": llc_schema.convert(self.llc_item, config.SCHEMA_VERSION),
            "cancelled": self.cancelled
        }

    def to_display_dict(self):
        return {
            "id": self.id,
            "display_id": encode_charge_id(self.id)
        }


class LocalLandChargeHistory(db.Model):
    __tablename__ = 'local_land_charge_history'

    id = db.Column(db.BigInteger, primary_key=True)
    llc_item = db.Column(JSONB, nullable=False)
    cancelled = db.Column(db.Boolean, nullable=False)
    item_changes = db.Column(JSONB)
    entry_number = db.Column(db.BigInteger, primary_key=True, index=True)
    entry_timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, llc_item, cancelled, item_changes, entry_number, entry_timestamp):
        self.id = id
        self.llc_item = llc_item
        self.cancelled = cancelled
        self.item_changes = item_changes
        self.entry_number = entry_number
        self.entry_timestamp = entry_timestamp

    def to_dict(self):
        history = {
            "entry-timestamp": self.entry_timestamp.isoformat(),
            "cancelled": self.cancelled,
            "entry-number": self.entry_number
        }

        if self.item_changes is not None:
            history["item-changes"] = self.item_changes

        if "author" in self.llc_item:
            history["author"] = self.llc_item["author"]

        return history


class GeometryFeature(db.Model):
    __tablename__ = 'geometry_feature'

    id = db.Column(db.BigInteger, primary_key=True)
    local_land_charge_id = db.Column(db.BigInteger, db.ForeignKey('local_land_charge.id'), primary_key=True)
    local_land_charge = db.relationship('LocalLandCharge', back_populates='geometry', uselist=False)
    geometry = db.Column(Geometry(srid=27700), nullable=False)

    def __init__(self, local_land_charge, geometry):
        self.local_land_charge = local_land_charge
        self.geometry = geometry
