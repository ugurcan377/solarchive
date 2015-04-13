import random
import solconfig


def roll_d10():
    return random.randint(1, 10)


def roll_d100():
    return random.randint(1, 100)

# def roll_on_table(table):
#     roll = roll_values(table["values"])
#     step_type = table["type"]
#     result = find_result(table["values"], roll)
#     if step_type == "background":
#         return "background", table["package"][result], table["morph"][result], table["next"][result]
#     data_type = solconfig.data_types[step_type]
#     return data_type, table[data_type][result]