import json
import solconfig


def get_data(name):
    res = solconfig.get_data_file(name)
    if res is None:
        raise Exception("Data file does not exists")
    return json.load(res)


general = get_data("general")
lifepath = get_data("lifepath")
packages = get_data("packages")
morphs = get_data("morphs")
gear = get_data("gear")
psi = get_data("psi")
traits = get_data("traits")
targets = {"aptitudes": "packages",
           "languages": "ep",
           "background": "packages",
           "customization": "packages",
           "focus": "packages",
           "faction": "packages",
           'synthmorph': 'ep'
           }
all_data = {"ep": general, "lifepath": lifepath, "packages": packages, "morphs": morphs}


def search(data, query):
    for k, v in data.iteritems():
        if k == query:
            return v
        elif type(v) == dict:
            res = search(v, query)
            if res:
                return res
    else:
        return False


def search_all(query):
    for data in all_data.values():
        res = search(data, query)
        if res:
            return res
    else:
        return False