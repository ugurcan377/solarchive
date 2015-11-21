from flask_restful import Resource

from solarchive import data


class ListPackages(Resource):
    data_source = data.packages

    def get(self, category):
        items = self.data_source.get(category)
        if not items:
            return {}, 404
        if type(items) == dict:
            keys = items.keys()
            keys.sort()
            item_list = []
            for key in keys:
                item = items[key]
                item.update({"name": key})
                item_list.append(item)
            items = item_list

        return {"items": items}


class GetPackages(Resource):
    data_source = data.packages

    def get(self, category, name):
        items = self.data_source.get(category)
        if not items:
            return {}, 404
        name = name.replace("_", " ")
        if name in items:
            item = items[name]
            item.update({"name": name})
            return item
        else:
            return {}, 404
