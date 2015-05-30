solarchive
==========

A companion program for Eclipse Phase RPG  
I deliberately seperated the system data from the program itself. You can find the data in *data/* folder in JSON format. If you want to create another software for Eclipse Phase you are welcome to use them.
While under active development i have most of data needed for package and life path creation system.  

##System Data Documentation
You will see four different files under the data folder 
+ data/packages.json : Packages for package base character creation (p. 15-38, Transhuman)
+ data/lifepath.json : Steps for the life path character creation system (p. 53-73, Transhumen)
+ data/ep.json : Generic data related to EP system morph/skill lists etc.
+ data/morphs.json : Morph statistics which will be required to properly create a character  
  (p. 6-111, Morph Recognition Guide)

###Packages Format
General format of packages file is like this
```json
{
    "package_type": {
        "package_name": {
            "attribute" : "value"
        }
    }
}
```
There are 5 package types "aptitudes", "background", "faction", "focus", "customization"
####Type: Aptitudes
There is only aptitude objects in aptitudes type
An aptitude object containes simply the name of the aptitude as key and a number which will be added to or subtracted from that aptitude as value  
  
**Example**
```json
{
    "aptitudes": {
        "brawler": {
            "aptitude": {
                "cog": 10,
                "coo": 20,
                "int": 15,
                "ref": 20,
                "sav": 10,
                "som": 20,
                "wil": 10
            },
            "longdesc": "lorem ipsum"
        }
    }
}
```
####Type: Background, Faction, Focus
These three type uses the same format
```json
{
    "package_name": {
        "longdesc": "lorem ipsum",
        "motivations": {
            "positive": [],
            "negative": []
        },
        "1": {},
        "3": {},
        "5": {}
    }
}
```
Package names uses this convention: lower-case, without colons or dashes  
On Transhuman a package usually have different values like 1PP, 3PP, 5PP "1", "3", "5" keys are used to represent this values.  
Packages contains different keys which represents different aspects of characters. The keys are "skills", "moxie", "rep", "aptitude", "trait", "credits" and "psi"  
+ aptitude is an object which has described before
+ rep is a number. "rep" denotes a network of players choice. If it was a specific network it will be "@-rep" for example
+ moxie and "credits" are numbers
+ trait is an array of strings if there is different levels for a trait this notation is used trait, traitv2, traitv3 + longdesc is the detailed description of the package as in the Transhuman sourcebook
+ psi is either a number or an object. If it's a number, player can select this number of sleights regardless of sleights type, and it's an object it tells the player how many sleights of which type they can choose. Exp. *"psi": {"chi": 3, "gamma": 3}*
+ skills is an object it contains the name of skill as key and a number, array or object as value. The skills which does not have different fields are always represented with numbers. Skills that does have different fields are represented by either a number or an object. A number means player chooses the field and an object means a pre-selected specific field. If the skill value is an array this means multiple fields on that same skill.
```json
{
    "skills": {
        "free fall": 30,
        "networking": 30, 
        "networking": {"value": 40, "spec": "scientists"}, 
        "academics": [40, 30], 
        "profession": [
            {"value": 50, "spec": "forensics"}, 
            {"value": 40, "spec": "police procedures"}
        ],
    }
}
```
  
1PP packages generally comes with 3 skills and sometimes a moxie point they rarely include rep, trait or aptitude.  
3PP packages generally comes with 5 to 10 skills and 50 rep of some type and sometimes a moxie point.  
5PP packages generally comes with 7 to 15 skills, 50 rep of some type, 5 aptitude of some type and a moxie point also sometimes with a trait

####Type: Customization
Customization type is just like background, faction, focus types but it does not have motivations field and since all customization packages are worth 1PP it does not have package value objects.

###Lifepath Format
General format of lifepath file is like this
```json
{
    "table_name": {
        "attribute" : "value"
    }
}
```
Tables names are strings that denotes steps for the life path system. Like "3","3.1", "6.5" etc. the only exception is a table name called "gatecrashing"  
There is no types like package_type but different steps may contain different attributes or values. It will be useful to think attributes as columns for each table. Because of that all values are arrays. Typical attributes are
+ title is the name of the step which is written in the Transhuman Sourcebook
+ type is a string which explains the tables purpose. It's sole purpose is to save developers from the effort to determine which table has what attributes
  + general is for tables which does not need specific action. Required attributes is values and tables. 
  + branching is for tables requires extra action. It usually leads to another tables according to the result. It containes following attributes: values, desc, action
  + background is only used for step 3. It has following attributes: values, desc, table, morph, next
  * event is used when it's an event table. It has same attributes with general but table is a list of objects and every object has the attributes desc and effect
  * info is used for general system info. It's just used for plain key-value storage
+ values represent results of dice rolls. Result could be a number or a range between two numbers ex. *[1, 2, 3, 4, 5, [6, 10]]*
+ desc is a string explains what will happen for that result
+ target is a string explains what the values on table (or sometimes action) is. Is it a language, an aptitude package, a faction package or background package etc.  
+ next in table\_name object means the next path for character Only used in step 3. If used in an object except the table\_name it means a roll has to be made in the table\_name which is in the value of next
+ morph is starting morph for character 
+ action means its'a branching table which tells how to continue. It has attributes like next, select, roll. Select means how many PP will the selected packages be and roll attribute is used if multiple rolls needed on the table designated in next
+ table is a generic column used store results of rolls from different tables. If it's a event table results will be objects with desc and effect attributes. Desc will explain what will happen to the character and effect how they will be effected from this. Will they gain a trait, new skill, lose money etc. 
```json
{
    "1": {
        "title": "Aptitude Template",
        "type": "general",
        "values": [1, 2, 3, 4, 5, 6, 7, 8, [9, 10]],
        "target": "aptitudes",
        "table": ["brawler", "dilettante", "extrovert", "inquisitive", "researcher", "survivor", "techie", "thrill seeker", {"next": "1"}]
    },
    "3": {
        "title": "Youth Path",
        "type": "branching",
        "values": [[1, 6], [7, 9], 10],
        "desc": ["Wholesome Youth", "Split Youth", "Fractured Youth"],
        "action": [{"next": "3.1", "select": 3}, {"next": "3.1", "roll": 2, "select": 1}, {"next": "3.1", "roll": 3, "select": 1}]
    },
    "3.6": {
        "title": "Sunward Childhood",
        "type": "background",
        "target": "background",
        "values": [1, [2, 3], [4, 6], [7, 10]],
        "desc": ["Pioneer dynasty", "Venusian colonist: privileged homesteader", "Venusian colony staff", "Mercurian slave labor"],
        "table": ["hyperelite scion", "fall evacuee enclaver", {"next": "3.10"}, "indenture"],
        "morph": ["exalt", "splicer", "", {"values": [[1, 7], [8, 10]], "table":["flat", "case"]}],
        "next": ["6.5", "6.6", "", "6.7"]
    },
    "6.2": {
        "title": "Autonomist",
        "type": "general",
        "target": "focus",
        "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "table": ["academic", "activist", "bot jammer", "covert ops", "explorer", "genehacker", "hacker", "medic", "scientist", "techie"]
    },
    "7": {
        "title": "Pre-Fall Life Event",
        "type": "event",
        "values": [[1, 20], [21, 22], [23, 24], [25, 26], [27, 28], [29, 30], [31, 32], [33, 34], [35, 36], [37, 38], [39, 40], [41, 42], [43, 44], [45, 46], [47, 48], [49, 50], [51, 52], [53, 54], [55, 56], [57, 58], [59, 60], [61, 62], [63, 64], [65, 66], [67, 68], [69, 70], [71, 72], [73, 74], [75, 76], [77, 78], [79, 80], [81, 82], [83, 84], [85, 86], [87, 88], [89, 90], [91, 92], [93, 94], [95, 96], [97, 98], [99, 100]],
        "table": [
            {"desc": "Gain +1 Moxie and roll on the Story Event table ", "effect": {"moxie": 1, "next": "16"}},
            {"desc": "You save an animal from danger. Gain the Animal Empathy trait ).", "effect": {"trait": "animal empathy"}},
            {"desc": "You take up a sport. +10 to Climbing, Fray, Free Fall, Freerunning, or Swimming.", "effect": {"skills": {"fray": 10}}},
            {"desc": "Your inability to improve holds you back from an important promotion/advancement. Gain the Slow Learner trait ).", "effect": {"trait": "slow learner"}},
            {"desc": "You simply are not very comfortable with that whole resleeving thing. Gain the Morphing Disorder (Level 1) trait ).", "effect": {"trait": "morphing disorder"}},
            {"desc": "You are not a slacker. You take on part-time jobs or additional training. +20 to one skill.", "effect": {"skills": {"any": 20}}},
            {"desc": "You travel extensively. +10 to two different Language skills.", "effect": {"skills": {"language": [10, 10]}}},
            {"desc": "Regular attention to your health and exercise improves your abilities. Gain +5 SOM.", "effect": {"aptitude": {"som": 5}}},
            "...",
            {"desc": "You make some life decisions that prove prescient after the Fall. Gain 20,000 credits.", "effect": {"credits": 20000}}
        ]
    },
}
```
###Morhps Format 
General format for morphs file is like this
```json
{
  "morph_name": {
      "class": "",
      "implants": [],
      "movement": {},
      "max_apt": 0,
      "durability": 0,
      "wt": 0,
      "advantages": {},
      "disadvantages": {},
      "notes": {},
      "cp": 0,
      "credit": ""
  }
}
```
Morph names uses the same naming conventions: lower case, no dashes
Contrary to other files all morhps contains the same fields:
"class", "implants", "movement", "max_apt", "durability", "wt", "advantages", "disadvantages", "notes", "cp", "credit"
+ class is a string to determine the class (or type) of morphs. İt can be "biomorph", "synthmorph", "pod"
+ implants tells what of enhancements does the morph have. It is always an array of strings. Few exp. "basic biomods", "basic mesh inserts", "bioweave armor (light)", "cortical stack" etc. 
+ movement tells how the morph moves around the environment. It is an object of arrays, key will be the name of way the morph moves (if the rulebook does not state a specific way the key will be "normal") and the value of movement is [int, int]. Ex. "Walker 4/20" -> {"walker": [4, 20]}
+ max_apt is the maximum aptitude for a morph. It is always an integer
+ durability is always an integer.
+ wt stands for Wound Threshold, it is always an integer.
+ advantages and disadvantages contains the definations which will effect a character's properties in a posivite or negative way. It uses keys aptitude, skills and trait as its described above plus two extra keys
    + armor key is used just like movement exp. 6/6 -> [6, 6]
    + some (beak, bite, claw, ramming etc.) attack is a states the morph has a special way to attack it dv and ap keys and value of ap is an integer and value of dv is an object which has two keys of its own (roll and bonus). In Eclipse Phase an attack is defined like this 2d10+4 dv -5 ap -> {"ap": -5, "dv": {"roll": 2, "bonus": 4}}. In a mathematical way roll is the coefficient of d10 and bonus is the constant 
+ notes is just like advantages or disadvantages but in mixed way, it is usually defines properties which are just different from the norm. They mostly could not be categorised as positive or negative
+ cp is an integer states the cost of the morph in EP Customization Points
+ credit is price of morph inside EP setting. It could state a cost class as string (moderate, high, expansive etc.) or a number if there is minimum price for the morph
```json
{
  "splicer": {
      "class": "biomorph",
      "implants": ["basic biomods", "basic mesh inserts", "cortical stack"],
      "movement": {"normal": [4, 20]},
      "max_apt": 25,
      "durability": 30,
      "wt": 6,
      "advantages": {"aptitude": {"any": 5}},
      "disadvantages": {},
      "notes": {},
      "cp": 10,
      "credit": "high"
  }
}
```
##TO DO
####README
+ Add psi documentation

####Dataset:
+ Add weapons and armor
+ Add gear (packages)
+ Add morph implants There is a list of them in Morph Recognition Guide
+ Add trait explanations  
Maybe in a distant future:
+ Add habıtat info
+ Add exoplanet info
+ Add vehicle info

####Core Program:
+ Decide and implement for how to represent characters
+ Implement the original (CP based) character creation system
+ Implement the plain packages character creation system
+ Develop a search algorithm for the future knowledge base

####Lifepath:
+ Prevent getting duplicate result when rolling on the same table more than once
+ STEP 6: Implement special clauses for table 6.12
+ STEP 8: If result contains a package insert it to step 9
+ STEP 9: AGI/Uplift characters should use 9.14 as faction table
+ STEP 11: If result contains a package insert it to step 10

####Web interface:
+ Design a user interface
+ Design a web api
+ Decide for backend technology (Probably Flask)
+ Decide for frontend technology (Probably react.js)

##Contributing
If you want to contribute or just report bugs feel free to send a pull request or open an issue.  
You can also drop me an email at ugurcanergn@gmail.com
##License and Attribution
Source code is distributed with one of the argonauts favorite licenses GNU GPLv2  
Eclipse Phase is a trademark of Posthuman Studios LLC  
All material related to Eclipse Phase is licenced with Creative Commons 3.0 BY-NC-SA
