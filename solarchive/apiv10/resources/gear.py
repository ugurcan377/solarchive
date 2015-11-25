from flask_restful import Resource

from solarchive.apiv10.resources.common import parser
from solarchive import data


class ListGear(Resource):
    data_source = data.gear
    have_categories = True

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
                if categorize and args.category not in item["category"]:
                    continue
                item.update({"name": key})
                item_list.append(item)
            items = item_list

        return {"items": items}


class GetGear(Resource):
    data_source = data.gear

    def get(self, name):
        name = name.replace("_", " ")
        if name in self.data_source:
            item = self.data_source[name]
            item.update({"name": name})
            return item
        else:
            return {}, 404