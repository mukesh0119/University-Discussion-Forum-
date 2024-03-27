# application/__init__.py
from flask import Flask
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_ckeditor import CKEditor

login_manager = LoginManager()
app = None

def create_app():

    global app

    if app is not None:
        return app
    
    app = Flask(__name__)

    # Load environment variables 
    load_dotenv()

    ckeditor = CKEditor(app)
    ckeditor.FormatSource = False

    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)
    print(app.config)


    login_manager.init_app(app)

    with app.app_context():
    	
        from .frontend import frontend_blueprint
        app.register_blueprint(frontend_blueprint)

        return app
