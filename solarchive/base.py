
class Character(object):
    def __init__(self):
        self.name = ""
        self.background = ""
        self.faction = ""
        self.motivations = {"positive": [], "negative": []}
        self.morph = "" #Probably need a morph class in the future
        self.aptitudes = {"cog": 0, "coo": 0, "int": 0, "ref": 0, "sav": 0, "som": 0, "wil": 0}
        self.stats = {"moxie": 0, "tt": 0, "luc": 0, "ir": 0, "wt": 0, "dur": 0, "dr": 0, "init": 0,
            "spd": 0, "dr": 0}
        self.skills = {}
        self.rep = {}
        self.trait = [] #Probably will need to seperate it as positive and negative

class Morph(object):
    pass

