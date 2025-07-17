# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from .config import Config
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    # When creating the app, we specify the location of the static and templates folders.
    # This is the crucial fix.
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))
                
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    Swagger(app)
    jwt.init_app(app)

    # Import and register both blueprints
    from .routes import main as main_blueprint, api as api_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)

    from . import models

    return app

