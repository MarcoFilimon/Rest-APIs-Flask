import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import PlainStoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
	@blp.response(200, PlainStoreSchema)
	def get(self, store_id):
		try:
			return stores[store_id] #! a specific store based on ID
		except KeyError:
			abort(404, message="Store not found")

	def delete(self, store_id):
		try:
			del stores[store_id]
			return {"message": "Store deleted."}
		except KeyError:
			abort(404, message="Store not found")


@blp.route("/store")
class StoreList(MethodView):
	@blp.response(201, PlainStoreSchema(many=True))
	def get(self):
		return stores.values() #! all stores

	@blp.arguments(PlainStoreSchema)
	@blp.response(200, PlainStoreSchema)
	def post(self, store_data):
		for store in stores.values():
			if store_data["name"] == store["name"]:
				abort(400, message=f"Store already exists.")

		store_id = uuid.uuid4().hex
		store = {**store_data, "id": store_id}
		stores[store_id] = store

		return store
