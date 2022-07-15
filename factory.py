from flask import Flask

from bp.application import app_bp
from bp.database import database_bp
from extensions import db, sess

# Add blueprints here
blueprints = [database_bp, app_bp]


def application():

    # Declarative Configuration
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///safe/database.db"
    app.config["SQLALCHEMY_BINDS"] = {
        "persistency": "sqlite:///safe/persistency.db"
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Session Configuration
    app.config["SESSION_COOKIE_DOMAIN"] = "e-core.com"

    # Init Extensions
    db.init_app(app)
    sess.init_app(app)

    # Register blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
