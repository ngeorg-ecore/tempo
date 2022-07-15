from flask import Blueprint

database_bp = Blueprint('database_bp', __name__, url_prefix="/safe", template_folder='templates', static_folder="static")

from .routes import *