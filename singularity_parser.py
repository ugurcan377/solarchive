import re

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
                tmp = {"value": int(value)}
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


def parse_traits(trait_str):
    if trait_str == "NONE":
        return ""
    trait_list = []
    split_traits = trait_str.split(",")
    for trait in split_traits:
        if trait and trait != " ":
            if "=" in trait:
                name, spec = trait.split("=")
                trait_list.append({"name": name, "spec": spec})
            else:
                trait_list.append(trait)
    if len(trait_list) == 1:
        return trait_list[0]
    else:
        return trait_list


def parse_morphs(morph_str):
    if not morph_str or morph_str == "ANY":
        return ""
    return [morph for morph in morph_str.split(",")]


def parse_ap(ap_str):
    ap_str = ap_str.replace('--', '0')
    if ap_str == "AVx2":
        return ap_str
    elif ap_str == "double":
        return "AVx2"
    elif 'or' in ap_str:
        return [int(x) for x in ap_str.split(" or ")]
    elif re.match('-?[0-9]', ap_str):
        return int(ap_str)
    return ap_str


def parse_dv(dv_str):
    if dv_str in ["--", "no damage"]:
        return 0
    elif dv_str.strip() == "Pain (see desc) or 2d10":
        return "Pain or 2d10"
    return dv_str


def parse_linked_skill(skill_str):
    if skill_str == "Unarmed Combat":
        return "Unarmed"
    elif ":" in skill_str:
        strip_skill = [x.strip() for x in skill_str.split(":")]
        return {"name": strip_skill[0], "spec": strip_skill[1]}
    return skill_str


def parse_armor(armor_str):
    if armor_str:
        return [int(x) for x in armor_str.split("/")]
    else:
        return ""


def parse_replace_curre(rep_str):
    if rep_str == "TRUE":
        return False
    elif rep_str == "FALSE":
        return True
    else:
        return ""


def parse_aptitudes(apt_str):
    apt_dict = {}
    if apt_str:
        split_apts = apt_str.split(",")
        for apt in split_apts:
            if apt:
                value, name = apt.split(":")
                apt_dict[name] = int(value)
    return apt_dict


def get_gears(grouped):
    gears = {}
    for line in grouped["GEAR"]:
        gear, name, gear_type, ap, dv, firing_mode, ammo, linked_skill,\
        armor, replace_curre, dur, speed, apts, skills, morphs_allowed, cost, desc = line
        gears[name] = {
            "type": [x for x in gear_type.split(",")],
            "desc": desc,
            "ap": parse_ap(ap),
            "dv": parse_dv(dv),
            "firing_mode": firing_mode,
            "ammo": ammo,
            "linked_skill": parse_linked_skill(linked_skill),
            "armor": parse_armor(armor),
            "cumulative_armor": parse_replace_curre(replace_curre),
            "durability": dur,
            "speed": speed,
            "aptitude": parse_aptitudes(apts),
            "morphs": parse_morphs(morphs_allowed),
            "cost": cost
        }
    return gears


def get_backgrounds(grouped):
    backgrounds = {}
    for line in grouped["BACKGROUND"]:
        background, name, desc, skill_modifiers, moxy_adj, traits, morphs, credit_mod, rep_mod, _, _, _, _, _, _, _, _ = line
        backgrounds[name] = {
            "desc": desc,
            "skills": parse_skills(skill_modifiers),
            "moxie": int(moxy_adj),
            "trait": parse_traits(traits),
            "morphs": parse_morphs(morphs),
            "credits": int(credit_mod),
            "rep": int(rep_mod),
        }
    return backgrounds


def get_factions(grouped):
    factions = {}
    for line in grouped["FACTION"]:
        faction, name, desc, skill_modifiers, moxy_adj, traits, morphs, credit_mod, rep_mod, _, _, _, _, _, _, _, _ = line
        factions[name] = {
            "desc": desc,
            "skills": parse_skills(skill_modifiers),
            "moxie": int(moxy_adj),
            "trait": parse_traits(traits),
            "morphs": parse_morphs(morphs),
            "credits": int(credit_mod),
            "rep": int(rep_mod),
        }
    return factions


def get_morphs(grouped):
    morph_desc = {}
    for line in grouped["MORPH"]:
        name, desc = line[1], line[12]
        morph_desc[name] = {"desc": desc}
    from solarchive.data import morphs
    for name in morph_desc:
        morph_name = name.lower()
        if morphs.get(morph_name):
            morphs[morph_name].update(morph_desc[name])

    return morphs

def show_field(data_type, field):
    if data_type == "gear":
        for k,v in gear_dict.iteritems():
            if v[field] not in ["", {}]:
                print k, " > ",v["type"], " > ", v[field]
    else:
        if data_type == "background":
            data = background_dict
        else:
            data = faction_dict
        for k, v in data.iteritems():
            print k, " > ", v[field]


def generate_json(json_dict):
    from jinja2 import Template
    template = Template('''{
    {% for elem in keys -%}
    "{{elem}}": {
        {% for k,v in elements[elem].iteritems() -%}
            {% if v is string -%}
            "{{k}}": "{{v}}",
            {% else -%}
            "{{k}}": {{v}},
            {% endif -%}
        {% endfor -%}
        },
    {% endfor -%}
    }''')
    sorted_keys = json_dict.keys()
    sorted_keys.sort()
    return template.render(elements=json_dict, keys=sorted_keys)


grouped_data = group(fc_data)
gear_dict = get_gears(grouped_data)
background_dict = get_backgrounds(grouped_data)
faction_dict = get_factions(grouped_data)
morph_dict = get_morphs(grouped_data)

f = open("/home/sentinel/workspace/solarchive/morphs.json", "w")
f.write(generate_json(json_dict=morph_dict))
f.close()
# f = open("/home/sentinel/workspace/solarchive/background.json", "w")
# f.write(generate_json(json_dict=background_dict))
# f.close()
# f = open("/home/sentinel/workspace/solarchive/faction.json", "w")
# f.write(generate_json(json_dict=faction_dict))
# f.close()