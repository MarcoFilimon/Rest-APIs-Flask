from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    # @jwt_required()
    @blp.response(200, ItemSchema) #! decorator to validate the data that WE SEND (the API) to the client. It gets passed through the schema. Used also for documentation (Swagger)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id) #! get a specific item based on ID
        return item

    # @jwt_required()
    def delete(self, item_id):
        #! I can block certain endpoints if they don't have certain privileges.
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, message="Admin privilege required.")
        item = ItemModel.query.get_or_404(item_id) #! delete an item based on ID
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}, 200

    # @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id): #! update item
        item = ItemModel.query.get(item_id)
        #! If the item exists, update it.
        if item:
            if "price" in item_data:
                item.price = item_data["price"]
            if "name" in item_data:
                item.name = item_data["name"]
        else: #! create item if it doesn't exist
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):
    # @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all() #! get all items

    # @jwt_required(fresh=True) #! require JWT token to create an item
    @blp.arguments(ItemSchema) #! This is used for data validation with marshmallow for upcoming data from client.
    @blp.response(201, ItemSchema)
    def post(self, item_data): #! item_data is the validated data that came from schema. So if I used arguments() I need to have this extra argument here.
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item

    # @jwt_required()
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