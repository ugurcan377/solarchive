from flask import Blueprint
from flask_restful import Api
from solarchive.apiv10.resources import common
from solarchive.apiv10.resources import gear
from solarchive.apiv10.resources import packages

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

api.add_resource(common.ListMotivations, "/motivations/")
api.add_resource(common.GetMotivations, "/motivations/<name>/")
api.add_resource(common.ListBackgrounds, "/backgrounds/")
api.add_resource(common.GetBackgrounds, "/backgrounds/<name>/")
api.add_resource(common.ListFactions, "/factions/")
api.add_resource(common.GetFactions, "/factions/<name>/")
api.add_resource(common.ListMorphs, "/morphs/")
api.add_resource(common.GetMorphs, "/morphs/<name>/")
api.add_resource(common.ListTraits, "/traits/")
api.add_resource(common.GetTraits, "/traits/<name>/")
api.add_resource(common.ListPsi, "/psi/")
api.add_resource(common.GetPsi, "/psi/<name>/")
api.add_resource(common.ListSkills, "/skills/")
api.add_resource(common.GetSkills, "/skills/<name>/")
api.add_resource(gear.ListGear, "/gear/")
api.add_resource(gear.GetGear, "/gear/<name>/")
api.add_resource(packages.ListPackages, "/packages/<category>/")
api.add_resource(packages.GetPackages, "/packages/<category>/<name>/")

