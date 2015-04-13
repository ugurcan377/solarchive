from solarchive.data import lifepath, targets, all_data
from solarchive.utils import roll_d100, roll_d10


class Lifepath(object):

    def __init__(self):
        self.step = 1
        self.char = {}
        self.data = lifepath

    def start_path(self):
        result = self.step_1(self.get_table())
        self.char.update(result)

    def get_table(self):
        return self.data.get(str(self.step))

    def find_result_index(self, values, roll):
        for i, v in enumerate(values):
            if type(v) == int and v == roll:
                return i
            if type(v) == list and v[0] <= roll <= v[1]:
                return i
        else:
            return -1

    def roll_values(self, values):
        v = values[-1]
        if type(v) == list:
            v = v[1]
        if v == 10:
            return roll_d10()
        if v == 100:
            return roll_d100()

    def get_from_table(self, target, result):
        data_file = targets[target]
        target_table = all_data[data_file][target]
        return target_table.get(result)

    def step_1(self, table):
        values = table["values"]
        roll = self.roll_values(values)
        index = self.find_result_index(values, roll)
        result = table["table"][index]
        if type(result) == "dict":
            return self.step_1(table)
        else:
            return self.get_from_table(table["target"], result)

    #TODO Determine how to roll for external tables
    def step_2(self, table):
        values = table["values"]
        roll = self.roll_values(values)
        index = self.find_result_index(values, roll)