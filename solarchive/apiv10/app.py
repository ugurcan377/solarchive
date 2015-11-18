from flask import Blueprint
from flask_restful import Api
from solarchive.apiv10.resources import common

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

api.add_resource(common.Motivations, "/motivations/")
