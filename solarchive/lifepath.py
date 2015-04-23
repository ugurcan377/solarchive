from solarchive.data import lifepath, targets, all_data
from solarchive.utils import roll_d100, roll_d10, clear_package, get_last_background, get_pp


class Lifepath(object):
    STEPS = 6

    def __init__(self):
        self.step = 1
        self.next_step = None
        self.char = {}
        self.data = lifepath

    def start_path(self):
        for i in range(self.STEPS):
            self.char[self.step-1] = self.get_next_step()
            if self.next_step:
                self.step = self.next_step
                self.next_step = None

    def get_table(self):
        return self.data.get(str(self.step))

    def get_next_step(self):
        func = getattr(self, "step_{}".format(self.step), lambda x: None)
        result = func(self.get_table())
        self.step += 1
        return result

    def get_result(self, table):
        table_type = table.get("type", "general")
        if table_type == "branching":
            return table["action"]
        else:
            return table["table"]

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

    def get_from_target(self, target):
        data_file = targets.get(target, "lifepath")
        target_table = all_data[data_file][target]
        return target_table

    def roll_on_table(self, table, with_index=False):
        values = table["values"]
        roll = self.roll_values(values)
        index = self.find_result_index(values, roll)
        if with_index:
            return self.get_result(table)[index], index
        return self.get_result(table)[index]

    def step_1(self, table):
        result = self.roll_on_table(table)
        while type(result) == dict:
            result = self.roll_on_table(table)
        return {
            "title": table["title"],
            "desc": table.get("desc", result),
            "result": self.get_from_target(table["target"])[result]
        }

    def step_2(self, table):
        lang_table = self.get_from_target(table["target"])
        return {
            "title": table["title"],
            "desc": table.get("desc", ""),
            "result": self.roll_on_table(lang_table)
        }

    def step_3(self, table):
        result, index = self.roll_on_table(table, with_index=True)
        backgrounds = {}
        for i in range(result["roll"]):
            next_table = self.get_from_target(result["next"])
            next_result = self.roll_on_table(next_table)
            final_table = self.get_from_target(next_result["next"])
            final_result, final_index = self.roll_on_table(final_table, with_index=True)
            if type(final_result) == dict:
                if final_result.get("next"):
                    final_table = self.get_from_target(final_result["next"])
                    final_result, final_index = self.roll_on_table(final_table, with_index=True)
                else:
                    final_result = self.roll_on_table(final_result)
            target_table = self.get_from_target(final_table["target"])
            background = target_table[final_result]
            morph = final_table["morph"][final_index]
            if type(morph) == dict:
                morph = self.roll_on_table(morph)
            next = final_table["next"][final_index]
            if type(next) == dict:
                next = self.roll_on_table(next)
            backgrounds[i] = {
                "title": final_table["title"],
                "desc": final_table["desc"][final_index],
                "background": clear_package(background, result["select"]),
                "morph": morph,
                # ONLY THE FINAL NEXT VALUE COUNTS
                "next": next,
                }
        return {
            "title": table["title"],
            "desc": table.get("desc", "")[index],
            "result": backgrounds
        }

    def step_4(self, table):
        result = self.roll_on_table(table)
        have_more = result["effect"].pop("next", False)
        result_dict = {
            "title": table["title"],
            "desc": result.get("desc", ""),
            "result": result["effect"],
            "extra": {}
        }
        if have_more:
            if "change_background":
                next_table = self.get_from_target("3.2")
                next_result = self.get_from_target("background")["street rat"]
                next_index = 5
                backgrounds = self.char[3]["result"]
                last_bg_key = get_last_background(backgrounds)
                pp = get_pp(backgrounds[last_bg_key]["background"])
                self.char[3]["result"][last_bg_key] = {
                    "title": next_table["title"],
                    "desc": next_table["desc"][next_index],
                    "background": clear_package(next_result, pp),
                    "morph": next_table["morph"][next_index],
                    "next": next_table["next"][next_index],
                    }
            else:
                next_table = self.data[have_more]
                next_result = self.roll_on_table(next_table)
                result_dict["extra"].update({
                    "title": next_table["title"],
                    "desc": next_result.get("desc", ""),
                    "result": next_result["effect"],
                    })

        return result_dict

    #TODO Implement Advanced Age modifiers
    def step_5(self, table):
        result, index = self.roll_on_table(table, with_index=True)
        if index == 0:
            self.next_step = 8
        age = result["age"]
        return {
            "title": table["title"],
            "desc": table.get("desc", ""),
            "result": age + roll_d10()
        }

    #TODO Continue testing STEP 6
    def step_6(self, table):
        result, index = self.roll_on_table(table, with_index=True)
        if result["next"] == "prev":
            backgrounds = self.char[3]["result"]
            last_bg_key = get_last_background(backgrounds)
            next_table = self.get_from_target(backgrounds[last_bg_key]["next"])
        elif result["next"] == "6.1":
            branch_table = self.get_from_target("6.1")
            branch_result = self.roll_on_table(branch_table)
            next_table = self.get_from_target(branch_result["next"])
        else:
            next_table = self.get_from_target(result["next"])
        next_result, next_index = self.roll_on_table(next_table, with_index=True)
        target_table = self.get_from_target(next_table["target"])
        print target_table.keys(), next_result
        package = target_table[next_result]
        return {
            "title": table["title"],
            "desc": table.get("desc", "")[index],
            "result": {
                "title": next_table["title"],
                "desc": next_result,
                "result": package
            },
            "next": next_table["next"]
        }
