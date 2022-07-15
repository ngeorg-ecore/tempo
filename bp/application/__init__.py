from flask import Blueprint

app_bp = Blueprint('app_bp', __name__, template_folder='templates', static_folder="static")

from .routes import *