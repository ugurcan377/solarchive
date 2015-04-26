import random
from solarchive.data import lifepath, targets, all_data
from solarchive.utils import roll_d100, roll_d10, clear_package, get_last_background, get_pp


class Lifepath(object):
    STEPS = 9

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

    def get_random_morph(self, ignore=()):
        table = all_data['ep']['morphs']
        result = self.roll_on_table(table)
        morph_type = result['next']
        while morph_type in ignore:
            result = self.roll_on_table(table)
            morph_type = result['next']
        next_table = all_data['ep'][morph_type]
        next_result = self.roll_on_table(next_table)
        return next_result['desc']

    def step_1(self, table):
        result = self.roll_on_table(table)
        while type(result) == dict:
            result = self.roll_on_table(table)
        return {
            "title": table.get('title', ''),
            "desc": table.get("desc", result),
            "result": self.get_from_target(table["target"])[result]
        }

    def step_2(self, table):
        lang_table = self.get_from_target(table["target"])
        return {
            "title": table.get('title', ''),
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
                "title": final_table.get('title', ''),
                "desc": final_table["desc"][final_index],
                "background": clear_package(background, result["select"]),
                "morph": morph,
                # ONLY THE FINAL NEXT VALUE COUNTS
                "next": next,
                }
        return {
            "title": table.get('title', ''),
            "desc": table.get("desc", "")[index],
            "result": backgrounds
        }

    def step_4(self, table):
        result = self.roll_on_table(table)
        have_more = result["effect"].pop("next", False)
        result_dict = {
            "title": table.get('title', ''),
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
                    "title": next_table.get('title', ''),
                    "desc": next_table["desc"][next_index],
                    "background": clear_package(next_result, pp),
                    "morph": next_table["morph"][next_index],
                    "next": next_table["next"][next_index],
                    }
            else:
                next_table = self.data[have_more]
                next_result = self.roll_on_table(next_table)
                result_dict["extra"].update({
                    "title": next_table.get('title', ''),
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
            "title": table.get('title', ''),
            "desc": table.get("desc", ""),
            "result": age + roll_d10()
        }

    def step_6(self, table):
        result, index = self.roll_on_table(table, with_index=True)
        if result["next"] == "prev":
            backgrounds = self.char[3]["result"]
            last_bg_key = get_last_background(backgrounds)
            if backgrounds[last_bg_key]["next"] == '6.1':
                branch_table = self.get_from_target("6.1")
                branch_result = self.roll_on_table(branch_table)
                current_table = branch_result["next"]
                next_table = self.get_from_target(branch_result["next"])
            else:
                current_table = backgrounds[last_bg_key]["next"]
                next_table = self.get_from_target(backgrounds[last_bg_key]["next"])
        elif result["next"] == "6.1":
            branch_table = self.get_from_target("6.1")
            branch_result = self.roll_on_table(branch_table)
            current_table = branch_result["next"]
            next_table = self.get_from_target(branch_result["next"])
        else:
            current_table = result['next']
            next_table = self.get_from_target(result["next"])
        next_result, next_index = self.roll_on_table(next_table, with_index=True)
        target_table = self.get_from_target(next_table["target"])
        package = target_table[next_result]
        return {
            "title": table.get('title', ''),
            "desc": table.get("desc", "")[index],
            "result": {
                "title": next_table.get('title', ''),
                "desc": next_result,
                "result": package
            },
            "next": current_table
        }

    def step_7(self, table):
        result = self.roll_on_table(table)
        have_more = result["effect"].pop("next", False)
        ignore = result['effect'].pop('ignore', [])
        result_dict = {
            "title": table.get('title', ''),
            "desc": result.get("desc", ""),
            "result": result["effect"],
            "extra": {}
        }
        if have_more:
            morph = self.get_random_morph(ignore)
            result_dict['extra'].update({'morph': morph})

        return result_dict

    def step_8(self, table):
        result = self.roll_on_table(table)
        have_more = result["effect"].pop("next", False)
        package = result['effect'].pop('package', False)
        select = result['effect'].pop('select', False)
        result_dict = {
            "title": table.get('title', ''),
            "desc": result.get("desc", ""),
            "result": result["effect"],
            "extra": {}
        }
        if have_more:
            if have_more == 'morphs':
                morph = self.get_random_morph()
                result_dict['extra'].update({'morph': morph})
            else:
                next_table = self.get_from_target(have_more)
                next_result = self.roll_on_table(next_table)
                result_dict["extra"].update({
                    "title": next_table.get('title', ''),
                    "desc": next_result.get("desc", ""),
                    "result": next_result.get("effect") or next_result,
                    })
        if package:
            if select:
                result_dict.update({'next': {'focus': package, 'select': select}})
            else:
                result_dict.update({'next': {'focus': package}})

        return result_dict

    def step_9(self, table):
        result, index = self.roll_on_table(table, with_index=True)

        #TODO Reroll for same focus packages
        focus_table = self.get_from_target('9.1')
        focus_result, focus_index = self.roll_on_table(focus_table, with_index=True)
        if focus_result['next'] == 'prev':
            focuses = self.char.get(6, {'next': '6.1'})
            last_bg_key = get_last_background(focuses)
            if focuses["next"] == '6.1':
                branch_table = self.get_from_target("6.1")
                branch_result = self.roll_on_table(branch_table)
                next_focus = self.get_from_target(branch_result["next"])
            else:
                next_focus = self.get_from_target(focuses["next"])
        elif focus_result["next"] == "6.1":
            branch_table = self.get_from_target("6.1")
            branch_result = self.roll_on_table(branch_table)
            next_focus = self.get_from_target(branch_result["next"])
        next_focus_result = self.roll_on_table(next_focus)
        focus_target = self.get_from_target(next_focus['target'])
        focus_package = clear_package(focus_target[next_focus_result], result['focus'])

        faction_table = self.get_from_target('9.2')
        faction_result, faction_index = self.roll_on_table(faction_table, with_index=True)
        if faction_result['next'] == 'prev':
            #FIXME What to do if next_focus is 6.12 ?
            if next_focus['next'] == '6.1':
                next_focus['next'] = random.choice(['9.4', '9.5', '9.6', '9.7', '9.8', '9.9', '9.10',
                                                    '9.11', '9.12', '9.13'])
            next_faction = self.get_from_target(next_focus["next"])
        elif faction_result["next"] == "9.3":
            branch_table = self.get_from_target("9.3")
            branch_result = self.roll_on_table(branch_table)
            next_faction = self.get_from_target(branch_result["next"])
        next_faction_result = self.roll_on_table(next_faction)
        faction_target = self.get_from_target(next_faction['target'])
        faction_package = clear_package(faction_target[next_faction_result], result['faction'])

        return {
            "title": table.get('title', ''),
            "desc": table.get("desc", "")[index],
            "result": {
                'faction': {
                    'title': faction_table.get('title', ''),
                    'desc': '{}: {}'.format(faction_table['desc'][faction_index], next_faction_result),
                    'result': faction_package
                },
                'focus': {
                    'title': focus_table.get('title', ''),
                    'desc': '{}: {}'.format(focus_table['desc'][focus_index], next_focus_result),
                    'result': focus_package
                },
            },
        }
