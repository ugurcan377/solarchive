from flask_restful import Resource
from flask_restful import reqparse

from solarchive import data


parser = reqparse.RequestParser()
parser.add_argument("category", dest="category", help="Get items by given category")

class ListItems(Resource):
    data_source = None
    have_categories = False

    def get(self):
        items = self.data_source
        args = parser.parse_args()
        categorize = False
        if args.category and self.have_categories:
            args.category = args.category.replace("_", " ")
            categorize = True

        if type(items) == dict:
            keys = items.keys()
            keys.sort()
            item_list = []
            for key in keys:
                item = items[key]
                if categorize and item["category"] != args.category:
                    continue
                item.update({"name": key})
                item_list.append(item)
            items = item_list

        return {"items": items}


class GetItems(Resource):
    data_source = None

    def get(self, name):
        name = name.replace("_", " ")
        if name in self.data_source:
            item = self.data_source[name]
            item.update({"name": name})
            return item
        else:
            return {}, 404


class Skill(object):
    data_source = data.general["skills"]
    have_categories = True

    def __init__(self):
        skills = {}
        fields = data.general["field skills"]
        for key, value in self.data_source.iteritems():
            if key == "type":
                continue
            if key in fields:
                value["fields"] = fields[key]["table"]
            else:
                value["fields"] = []
            skills[key] = value
        self.data_source = skills

class ListMotivations(ListItems):
    data_source = data.general["motivations"]["table"]


class GetMotivations(GetItems):
    data_source = data.general["motivations"]["table"]


class ListDisorders(ListItems):
    data_source = data.general["disorder"]["table"]


class GetDisorders(GetItems):
    data_source = data.general["disorder"]["table"]


class ListBackgrounds(ListItems):
    data_source = data.general["backgrounds"]


class GetBackgrounds(GetItems):
    data_source = data.general["backgrounds"]


class ListFactions(ListItems):
    data_source = data.general["factions"]


class GetFactions(GetItems):
    data_source = data.general["factions"]


class ListMorphs(ListItems):
    data_source = data.morphs
    have_categories = True


class GetMorphs(GetItems):
    data_source = data.morphs


class ListTraits(ListItems):
    data_source = data.traits["traits"]
    have_categories = True


class GetTraits(GetItems):
    data_source = data.traits["traits"]


class ListPsi(ListItems):
    data_source = data.psi["psi"]["sleights"]
    have_categories = True


class GetPsi(GetItems):
    data_source = data.psi["psi"]["sleights"]


class ListSkills(Skill, ListItems):
    pass


class GetSkills(Skill, GetItems):
    pass
