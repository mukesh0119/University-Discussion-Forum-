# application/__init__.py
import config
import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = None

def create_app():
    
    global app

    if app is not None:
        return app

    app = Flask(__name__)

    # Load environment variables 
    load_dotenv()   

    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)
    
    db.init_app(app)

    with app.app_context():
        # Register blueprints
        from .post_api import post_api_blueprint
        app.register_blueprint(post_api_blueprint)

        from .models import Comment,Post
        db.create_all()
         
        return app
