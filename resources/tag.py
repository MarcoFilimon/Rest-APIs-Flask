from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import TagSchema, TagAndItemSchema
from models import TagModel, StoreModel, ItemModel

blp = Blueprint("Tags", __name__, description="Operations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id): #! get a list of tags under a specific store
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id): #! create a tag under a specific store
        # check that the store does not have a tag with the same name
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id): #!  Link an item in a store with a tag from the same store.
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store.id != tag.store.id:
            abort(400, message="Make sure item and tag belong to the same store before linking.")

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id): #! Unlink a tag from an item.
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "Tag removed from item", "item": item, "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id): # ! get a specific tag based on ID
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        200,
        description="Deletes a tag if no items are associated with it.",
        example={"message": "Tag deleted."}
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(400, description="Returned if the tag is assigned to one or more items. In this case, the tag cannot be deleted.")
    def delete(self, tag_id): #! Delete a tag, which must have no associated items.
        tag = TagModel.query.get_or_404(tag_id)
        if tag.items:
            abort(400, message="Tag cannot be deleted because it is assigned to one or more items.")
        db.session.delete(tag)
        db.session.commit()
        return {"message": "Tag deleted."}