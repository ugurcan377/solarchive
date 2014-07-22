import random
from solarchive.data import get_data

def roll_d10():
    return random.randint(1, 10)


def roll_d100():
    return random.randint(1, 100)


def find_result(values, roll):
    for i, v in enumerate(values):
        print v
        if type(v) == int and v == roll:
            return i
        if type(v) == list and v[0] <= roll <= v[1]:
            return i
    else:
        return -1
