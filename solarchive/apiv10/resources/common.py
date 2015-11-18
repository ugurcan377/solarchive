from flask_restful import Resource

from solarchive import data


class ListItems(Resource):
    data_source = None

    def get(self):
        items = self.data_source
        return {"items": items}


class GetItems(Resource):
    data_source = None

    def get(self, name):
        if name in self.data_source:
            item = self.data_source[name]
            item.update({"name": name})
            return item
        else:
            return {}, 404


class Motivations(ListItems):
    data_source = data.general["motivations"]["table"]


class Disorders(ListItems):
    data_source = data.general["disorder"]["table"]
