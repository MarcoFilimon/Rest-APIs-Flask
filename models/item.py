from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True) # primary key is automatically indexed by SQLAlchemy (starts from 1)
    name = db.Column(db.String(80), nullable=False) # nullable means that the field cannot be null in the database.
    description = db.Column(db.String(200), nullable=True) # description is optional, so it can be null.
    price = db.Column(db.Float(precision=2), nullable=False)

    # Every item belongs to a store, so we need to define the foreign key relationship.
    # The store_id column will be used to link the item to its store.
    # foreign key is a reference to the primary key of another table.
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)

    # The relationship between the item and the store is defined here.
    # back_populates is used to define a bidirectional relationship between the two models.
    # store model also has a relationship to the item model.
    # This allows us to access the store associated with an item.
    store = db.relationship("StoreModel", back_populates="items")

    tags = db.relationship("TagModel", secondary="items_tags", back_populates="items")