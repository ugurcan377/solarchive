import random
from solarchive import data


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


def get_skill_type(skill_name):
    if skill_name == 'any':
        return 'any'
    elif skill_name in data.general['field skills']:
        return 'knowledge'
    else:
        return 'active'


def get_trait_type(trait_name):
    return data.traits['traits'].get(trait_name)['category']


def parse_skills(skill_dict):
    """ Skill format will be [(skill name, value, type)]
    type 'knowledge', 'active' or 'any'
    """
    spec_format = '{}: {}'
    skill_list = []

    def format_skill(name, item):
        if type(item) is dict:
            if 'choices' in item:
                skill_list.append([spec_format.format('Choose', ', '.join(item['choices'])), item['value'],
                                   get_skill_type(name)])
            else:
                if 'category' in item:
                    selector = 'category'
                else:
                    selector = 'spec'
                skill_list.append([spec_format.format(name, item.get(selector)), item['value'], get_skill_type(name)])
        else:
            skill_list.append([name, item, get_skill_type(name)])

    for name, details in skill_dict.items():
        if type(details) is list:
            for item in details:
                format_skill(name, item)
        else:
            format_skill(name, details)
    return skill_list


def parse_traits(trait_list):
    """ Trait format will be [(name, nature, trait_type)]
    nature 'positive' or 'negative'
    trait_type type 'ego' or 'morph'
    """
    spec_format = '{}: {}'
    traits = []
    for trait in trait_list:
        if type(trait) is dict:
            nature, trait_type = get_trait_type(trait['name'])
            traits.append([spec_format.format(trait['name'], trait['spec']), nature, trait_type])
        else:
            nature, trait_type = get_trait_type(trait)
            traits.append([trait, nature, trait_type])
    return traits


gear_fields = {
    'drug': [],
    'weapon': ["linked_skill", "dv", "ap", "ammo", "firing_mode"],
    'toxin': [],
    'ammo': ["dv", "ap"],
    'service': [],
    'survival gear': [],
    'exploration gear': [],
    'nanodrug': [],
    'armor': ["armor", "morphs", "cumulative_armor"],
    'nanotechnology': [],
    'ai': [],
    'vehicles': [],
    'communication': [],
    'augmentation': ["aptitude", "morphs"],
    'pathogen': [],
    'seeker grenade': ["dv", "ap"],
    'scorcher': [],
    'armor mod': [],
    'weapon accessory': [],
    'espionage': [],
    'xenoarcheology gear': [],
    'pet': [],
    'alien relics': [],
    'exoskeleton': ["armor", "cumulative_armor"],
    'ai & muses': [],
    'narcoalgorithm': ["morphs"],
    'chemical': [],
    'robot': [],
    'nanotoxin': [],
    'grenade mod': [],
    'program': [],
    'scavenged tech': [],
    'sensor': [],
    'skillsoft': [],
    'everyday common': [],
    'psi-drug': ["morphs"]
}

gear_texts = {
    "linked_skill": "Skill",
    "dv": "DMG",
    "ap": "AP",
    "firing_mode": "Modes",
    "cumulative_armor": "Stackable",
}