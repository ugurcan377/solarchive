from flask import Flask
from flask import render_template

from solarchive import data
import solarchive.utils as utils
from solconfig import css_classes
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("layout.html")


@app.route('/backgrounds')
def backgrounds():
    skill_dict = {k:utils.parse_skills(v['skills']) for k,v in data.general['backgrounds'].items()}
    trait_dict = {k:utils.parse_traits(v['traits']) for k,v in data.general['backgrounds'].items()}
    temp_dict = {"data": data.general["backgrounds"],
                 "css": css_classes,
                 "title": "Backgrounds",
                 "act_backgrounds": "active",
                 "skill_dict": skill_dict,
                 "trait_dict": trait_dict,
                 }
    return render_template("backgrounds_factions.html", **temp_dict)

@app.route('/factions')
def factions():
    skill_dict = {k:utils.parse_skills(v['skills']) for k,v in data.general['factions'].items()}
    trait_dict = {k:utils.parse_traits(v['traits']) for k,v in data.general['factions'].items()}
    temp_dict = {"data": data.general["factions"],
                 "css": css_classes,
                 "title": "Factions",
                 "act_factions": "active",
                 "skill_dict": skill_dict,
                 "trait_dict": trait_dict,
                 }
    return render_template("backgrounds_factions.html", **temp_dict)


@app.route('/skills')
def skills():
    temp_dict = {"data": data.general["skills"],
                 "css": css_classes,
                 "title": "Skills",
                 "act_skills": "active",
                 "categories": [("active", ":not(.knowledge)"), ("knowledge", ".knowledge")],
                 }
    return render_template("skills.html", **temp_dict)


@app.route('/traits')
def traits():
    temp_dict = {"data": data.traits['traits'],
                 "css": css_classes,
                 "title": "Traits",
                 "act_traits": "active",
                 "categories": [("positive", ".positive"), ("negative", ".negative"), ("ego", ".ego"),
                                ("morph", ".morph"), ("positive ego", ".positive.ego"),
                                ("negative ego", ".negative.ego"), ("positive morph", ".positive.morph"),
                                ("negative morph", ".negative.morph")],
                 }
    return render_template("traits.html", **temp_dict)


@app.route('/psi')
def psi():
    temp_dict = {"data": data.psi['psi']['sleights'],
                 "css": css_classes,
                 "title": "Psi",
                 "act_psi": "active",
                 "categories": [("chi", ".chi"), ("gamma", ".gamma"), ("active", ".active"), ("passive", ".passive"),
                                ("active chi", ".active.chi"), ("passive chi", ".passive.chi"),
                                ("active gamma", ".active.gamma"), ("passive gamma", ".passive.gamma")],
                 }
    return render_template("psi.html", **temp_dict)


@app.route('/other/<key>')
def other(key):
    temp_dict = {"data": data.general.get(key, {}),
                 "title": "Other: {}".format(key.capitalize()),
                 "act_{}".format(key): "active"
                 }
    return render_template("other.html", **temp_dict)


@app.route('/gear')
def gear():
    temp_dict = {"data": data.gear,
                 "css": css_classes,
                 "gear_texts": utils.gear_texts,
                 "gear_fields": utils.gear_fields,
                 "title": "Gear",
                 "act_gear": "active",
                 "categories": [("augmentations", ".augmentation"), ("armor", ".armor, .exoskeleton"),
                                ("weapon", ".weapon"), ("ammo", ".ammo"), ("grenades and missles", ".seeker, .grenade"),
                                ("drugs and chemicals",".drugs, .toxin, .nanodrug, .pathogen, .narcoalgorithm, "
                                                       ".chemical, .nanotoxin, .psi-drug"),
                                ("tech", ".ai, .communication, .espionage, .robot, .program, .muses, .scavenged, "
                                         ".sensor, .skillsoft, .nanotechnology, .scorcher"), ("vehicles", ".vehicles"),
                                ("services", ".service"), ("everyday objects", ".everyday"),
                                ("survival and exploration", ".gear")],
                 }
    return render_template("gear.html", **temp_dict)


@app.route('/field_skills/<key>')
def field_skills(key):
    temp_dict = {"data": data.general['field skills'].get(key, {}),
                 "title": "Field Skills: {}".format(key.capitalize()),
                 "act_{}".format(key): "active"
                 }
    return render_template("other.html", **temp_dict)