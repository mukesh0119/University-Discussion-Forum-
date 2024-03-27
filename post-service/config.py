import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    # generated from secrets.token_urlsafe()
    SECRET_KEY = "uKHz_pkkYludL4d38Gf79Mxe-aRCALM6HglP78HCH8Q"
    SQLALCHEMY_TRACK_MODIFICATONS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    USER_SERVICE = "localhost:5001"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///posts-service.db'
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = True
    USER_SERVICE = "user-service:5001"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://post-service:pass1234@post-db:3306/post'
    SQLALCHEMY_ECHO = False
