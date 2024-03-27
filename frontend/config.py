import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = "3834j2724827"

class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    POST_SERVICE = "localhost:5002"
    USER_SERVICE = "localhost:5001"

class ProductionConfig(Config):
    ENV = "Production"
    DEBUG = True
    POST_SERVICE = "post-service:5002"
    USER_SERVICE = "user-service:5001"