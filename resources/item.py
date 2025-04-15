from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id) #! get a specific item based on ID
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id) #! delete an item based on ID
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}, 200

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id): #! update item
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data) #! create item if it doesn't exist
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all() #! get all items

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data): #! an create item
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item

    def delete(self): #! delete all items
        try:
            items = ItemModel.query.all()
            for item in items:
                db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()  # Rollback in case of an error
            abort(500, message="An error occurred while deleting the items.")
        return {"message": "All items have been deleted."}, 200