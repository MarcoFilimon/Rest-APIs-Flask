from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from jwt_callbacks import register_jwt_callbacks
from config import Config

from db import db
import models # used by the database to create the tables

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

# usage exmplaes
# app = create_app(config_object=MyCustomConfig) - with custom config class
# app = create_app(config_object=Config(db_url="postgresql://...")) - with config instannce
# app = create_app(db_url="postgresql://...") - just db_url

def create_app(db_url=None, config_object=None):
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    else:
        config = Config(db_url)
        app.config.from_object(config)
        # Ensure SQLALCHEMY_DATABASE_URI is set if using instance
        app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI

    db.init_app(app) #! initializes the db object with the app object.
    migrate = Migrate(app, db) #! initializes the migration object with the app and db objects.

    api = Api(app)

    jwt = JWTManager(app) #! initializes the JWT manager with the app object.
    register_jwt_callbacks(jwt)


    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app