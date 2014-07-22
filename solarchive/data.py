import json
import solconfig


def get_data(name):
    res = solconfig.get_data_file(name)
    if res is None:
        raise Exception("Data file does not exists")
    return json.load(res)


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
