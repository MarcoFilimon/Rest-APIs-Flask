from flask.views import MethodView
from flask_smorest import Blueprint, abort


from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route('/store/<int:store_id>')
class Store(MethodView):
	@blp.response(200, StoreSchema)
	def get(self, store_id):
		store = StoreModel.query.get_or_404(store_id)
		return store

	def delete(self, store_id):
		store = StoreModel.query.get_or_404(store_id)
		db.session.delete(store)
		db.session.commit()
		return {"message": "Store deleted."}, 200

@blp.route("/store")
class StoreList(MethodView):
	@blp.response(201, StoreSchema(many=True))
	def get(self):
		return StoreModel.query.all()

	@blp.arguments(StoreSchema)
	@blp.response(201, StoreSchema)
	def post(self, store_data):
		store = StoreModel(**store_data)
		try:
			db.session.add(store)
			db.session.commit()
		except IntegrityError:
			abort(
				400,
				message="A store with that name already exists.",
			)
		except SQLAlchemyError:
			abort(500, message="An error occurred creating the store.")

		return store

	def delete(self): #! delete all stores
		try:
			stores = StoreModel.query.all()
			for store in stores:
				db.session.delete(store)
			db.session.commit()
		except SQLAlchemyError:
			db.session.rollback()  # Rollback in case of an error
			abort(500, message="An error occurred while deleting the stores.")
		return {"message": "All stores have been deleted."}, 200

