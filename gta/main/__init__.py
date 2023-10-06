from flask import Blueprint
bp = Blueprint('main', __name__)
from gta.main import routes