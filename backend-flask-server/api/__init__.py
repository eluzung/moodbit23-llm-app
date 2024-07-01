# import individual routes
from flask import Blueprint
from api.openai import openai_bp
from api.wikipedia import wiki_bp
from api.web_scraping import web_scraping_bp
from api.split_json_data import json_bp
from api.indexing import indexing_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')
api_bp.register_blueprint(openai_bp)
api_bp.register_blueprint(wiki_bp)
api_bp.register_blueprint(web_scraping_bp)
api_bp.register_blueprint(json_bp)
api_bp.register_blueprint(indexing_bp)