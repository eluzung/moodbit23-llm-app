# import individual routes
from flask import Blueprint
from api.openai import openai_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')
api_bp.register_blueprint(openai_bp)

# wikipedia route will be here