import random


def roll_d10(with_bonus=False):
    if with_bonus:
        return random.randint(1, 10) % 10
    return random.randint(1, 10)


def roll_d100(with_bonus=False):
    if with_bonus:
        return random.randint(1, 100) % 100
    return random.randint(1, 100)


def clear_package(package, select):
    select = str(select)
    selects = ["1", "3", "5"]
    selects.remove(select)
    for s in selects:
        package.pop(s, 0)
    return package


def get_last_background(backgrounds):
    key_list = backgrounds.keys()
    key_list.sort()
    return key_list[-1]


def get_pp(package):
    key_list = package.keys()
    key_list.sort()
    selects = ["1", "3", "5"]
    select = filter(lambda x: x in selects, key_list)
    return select[0]
