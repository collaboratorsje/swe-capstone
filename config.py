from os import environ, path
from dotenv import load_dotenv

base = path.abspath(path.dirname(__file__))
load_dotenv(path.join(base, ".env"))
class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = environ.get("FLASK_DEBUG")
    FLASK_APP = "main.py"
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")