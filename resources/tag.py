from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import TagSchema
from models import TagModel, StoreModel

blp = Blueprint("Tags", __name__, description="Operations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):
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



@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id): # ! get a specific tag based on ID
        tag = TagModel.query.get_or_404(tag_id)
        return tag