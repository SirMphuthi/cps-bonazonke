# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from .config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    Swagger(app)
    jwt.init_app(app)

    from .routes import api as api_blueprint
    app.register_blueprint(api_blueprint)
    
    # --- ADD THIS LINE ---
    from . import models
    # ---------------------

    return app
