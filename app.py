from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask import jsonify
from flask_migrate import Migrate
import os

from db import db
import models
from blocklist import BLOCKLIST

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__) #! needs to be called "app" + also app.py

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API" #! mandatory to work.
    app.config["API_VERSION"] = "v1" #! mandatory to work.
    app.config["OPENAPI_VERSION"] = "3.0.3" #! mandatory to work.
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app) #! initializes the db object with the app object.

    migrate = Migrate(app, db) #! initializes the migration object with the app and db objects.
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "1035321680736365778000684778808813581" # to make sure the JWT tokens are signed and verified correctly.
    jwt = JWTManager(app) #! initializes the JWT manager with the app object.

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        #! this function checks if the token is in the blocklist.
        #! if it is, it returns True and the token is revoked.
        #! if it is not, it returns False and the token is not revoked.
        return jwt_payload["jti"] in BLOCKLIST

    #! I can add extra information to the JWT token when it is created.
    #! This is useful for adding user roles or permissions to the token.
    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     if identity == 1: #! admin user
    #         return {"is_admin": True}
    #     return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )
    # JWT configuration ends

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app