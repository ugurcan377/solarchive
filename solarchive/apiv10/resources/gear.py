from flask_restful import Resource

from solarchive import data


class ListGear(Resource):
    data_source = data.gear

    def get(self):
        items = self.data_source
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