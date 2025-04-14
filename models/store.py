from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # The items relationship is defined here. It allows us to access the items associated with a store.
    # lazy="dynamic" allows for further filtering and querying of the items relationship
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    # cascade="all, delete" means that if a store is deleted, all its items will also be deleted.

    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")