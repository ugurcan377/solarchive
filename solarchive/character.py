from solarchive.data import general, morphs

class Character(object):
    def __init__(self, cp=1000):
        self.cp = cp
        self.meta = {
            "background": "",
            "faction": "",
            "age": 0,
            "motivations": {}
        }
        self.aptitude = {}
        self.stats = {"moxie": 1, "speed": 1}
        self.skills = {}
        self.rep = {}
        self.trait = []
        self.sleights = []
        self.gear = []
        self.morph = {}
        self.credits = 0

    def set_default_aptitudes(self):
        self.aptitude = {
            "cog": 15,
            "coo": 15,
            "int": 15,
            "ref": 15,
            "sav": 15,
            "som": 15,
            "wil": 15
        }

    def get_linked_aptitude(self, skill):
        skill = general["skill list"].get(skill)
        if skill:
            return skill["linked"]
        else:
            return skill

    def calculate_stats(self):
        luc = self.aptitude["wil"] * 2
        dur = self.morph["durability"]
        dr = dur * 1.5
        if self.morph["class"] == "synthmorph":
            dr = dur * 2
        init = (self.aptitude["int"] + self.aptitude["ref"]) * 2
        stats = {
            "tt": luc / 5,
            "luc": luc,
            "ir": luc * 2,
            "wt": dur / 5,
            "dur": dur,
            "dr": dr,
            "init": init,
            "db": dur / 10
        }
        self.stats.update(stats)

    def get_morph_by_name(self, morph_name):
        return morphs.get(morph_name)