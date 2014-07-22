import os
import inspect


def get_root_dir():
    pth = os.path.abspath(inspect.getsourcefile(lambda x: x))
    return os.path.dirname(pth)

data_path = "data"
data_files = {
    "general": "ep.json",
    "lifepath": "lifepath.json",
    "packages": "packages.json"
}


def get_data_file(name):
    fn = data_files.get(name)
    if fn is None:
        return None
    fpath = os.path.join(get_root_dir(), data_path, fn)
    return open(fpath)
