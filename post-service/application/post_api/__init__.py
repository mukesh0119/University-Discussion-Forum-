# application/post_api/__init__.py
from flask import Blueprint

post_api_blueprint = Blueprint('post_api', __name__)

from . import routes

