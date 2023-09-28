from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

gta = Flask(__name__)

gta.secret_key = 'dev'    
gta.config["FLASK_ENV"] = "development"
gta.config["DEBUG"] = True

gta.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy()
db.init_app(gta)

bootstrap = Bootstrap5(gta)

login_manager = LoginManager()
login_manager.init_app(gta)
login_manager.login_view = "LoginPage"

from GTAApplication.models import models
from GTAApplication.forms import forms