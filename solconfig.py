import os
import inspect


def get_root_dir():
    pth = os.path.abspath(inspect.getsourcefile(lambda x: x))
    return os.path.dirname(pth)

data_path = "data"
data_files = {
    "general": "ep.json",
    "lifepath": "lifepath.json",
    "packages": "packages.json",
    "morphs": "morphs.json",
    "gear": "gear.json",
    "psi": "psi.json",
    "traits": "traits.json",

}


def get_data_file(name):
    fn = data_files.get(name)
    if fn is None:
        return None
    fpath = os.path.join(get_root_dir(), data_path, fn)
    return open(fpath)

data_types = {
    "general": ["values", "table"],
    "package": ["values", "package"],
    "branching": ["values", "desc", "action"],
    "background": ["values", "desc", "package", "morph", "next"],
    "event": ["values", "table"]
}
