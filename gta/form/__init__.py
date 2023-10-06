from flask import Blueprint, current_app
bp = Blueprint('form', __name__)
from gta.form import routes, forms