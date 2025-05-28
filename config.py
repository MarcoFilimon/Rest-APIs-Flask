import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
env_file = os.path.join(basedir, '.env')
load_dotenv(env_file)

class Config:
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Stores REST API" #! mandatory to work.
    API_VERSION = "v1" #! mandatory to work.
    OPENAPI_VERSION = "3.0.3" #! mandatory to work.
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self, db_url=None):
        self.SQLALCHEMY_DATABASE_URI = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")

    JWT_SECRET_KEY = "1035321680736365778000684778808813581" # to make sure the JWT tokens are signed and verified correctly.