# Comment out line 2128 2129
f = open("epdata.txt")
raw_data = f.readlines()
fc_data = [line.strip() for line in raw_data if line.startswith("#") == False]

def group(dataset):
    splitted = map(lambda x: x.split("|"), dataset)
    grouped = {}
    for s in splitted:
        data_type = grouped.get(s[0], [])
        data_type.append(s)
        grouped[s[0]] = data_type
    return grouped

def parse_skills(skill_str):
    skill_dict = {}
    if skill_str:
        split_skills = skill_str.split(",")
        for skill in split_skills:
            if skill:
                value, name = skill.split(":")
                choices, spec, category = [], "", ""
                if "#" in name:
                    choices = name.split("#")
                    name = "any"
                if "=" in name:
                    name, spec = name.split("=")
                if name.isupper():
                    if name in ["NETWORKING", "ANY"]:
                        name = name.lower().capitalize()
                    else:
                        category = name
                        name = "any"
                tmp = {"value": value}
                if choices:
                    tmp["choices"] = choices
                if spec:
                    tmp["spec"] = spec
                if category:
                    tmp["category"] = category
                if skill_dict.get(name):
                    existing = skill_dict[name]
                    if type(existing) == list:
                        skill_dict[name].append(tmp)
                    else:
                        skill_dict[name] = [existing, tmp]
                else:
                    skill_dict[name] = tmp
        return skill_dict
    else:
        return {}


def get_gears(grouped):
    gears = {}
    for line in grouped["GEAR"]:
        gear, name, gear_type, ap, dv, firing_mode, ammo, linked_skill,\
        armor, replace_curre, dur, speed, apts, skills, morphs_allowed, cost, desc = line
        gears[name] = {
            "type": gear_type,
            #"desc": desc,
            "ap": ap,
            "dv": dv,
            "firing_mode": firing_mode,
            "ammo": ammo,
            "linked_skill": linked_skill,
            "armor": armor,
            "replace_curre": replace_curre,
            "durability": dur,
            "speed": speed,
            "aptitudes": apts,
            "skills": skills,
            "morphs_allowed": morphs_allowed,
            "cost": cost
        }
    return gears

def get_backgrounds(grouped):
    backgrounds = {}
    for line in grouped["BACKGROUND"]:
        background, name, desc, skill_modifiers, moxy_adj, traits, morphs, credit_mod, rep_mod, _, _, _, _, _, _, _, _ = line
        backgrounds[name] = {
            #"desc": desc,
            "skills": parse_skills(skill_modifiers),
            "moxy_adj": moxy_adj,
            "traits": traits,
            "morphs": morphs,
            "credit_mod": credit_mod,
            "rep_mod": rep_mod,
        }
    return backgrounds

def get_factions(grouped):
    factions = {}
    for line in grouped["FACTION"]:
        faction, name, desc, skill_modifiers, moxy_adj, traits, morphs, credit_mod, rep_mod, _, _, _, _, _, _, _, _ = line
        factions[name] = {
            #"desc": desc,
            "skills": parse_skills(skill_modifiers),
            "moxy_adj": moxy_adj,
            "traits": traits,
            "morphs": morphs,
            "credit_mod": credit_mod,
            "rep_mod": rep_mod,
        }
    return factions

grouped_data = group(fc_data)
gear_dict = get_gears(grouped_data)
background_dict = get_backgrounds(grouped_data)
faction_dict = get_factions(grouped_data)
