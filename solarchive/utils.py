import random


def roll_d10():
    return random.randint(1, 10)


def roll_d100():
    return random.randint(1, 100)


def find_result(values, roll):
    for i, v in enumerate(values):
        if type(v) == int and v == roll:
            return i
        if type(v) == list and v[0] <= roll <= v[1]:
            return i
    else:
        return -1


def determine_dice(values):
    v = values[-1]
    if type(v) == list:
        v = v[1]
    if v == 10:
        return roll_d10
    if v == 100:
        return roll_d100
