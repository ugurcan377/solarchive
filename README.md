solarchive
==========

A companion program for Eclipse Phase RPG  
I deliberately seperated the system data from the program itself. You can find the data in *data/* folder in JSON format. If you want to create another software for Eclipse Phase you are welcome to use them.
While under active development i have most of data needed for package and life path creation system.  

##System Data Documentation
You will see three different files under the data folder 
+ data/packages.json : Packages for package base character creation (p. 15-38, Transhuman)
+ data/lifepath.json : Steps for the life path character creation system (p. 53-73, Transhumen)
+ data/ep.json : Generic data related to EP system morph/skill lists etc.

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
            }
        }
    }
}
```
####Type: Background, Faction, Focus
These three type uses the same format
```json
{
    "package_name": {
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
+ trait is an array of strings if there is different levels for a trait this notation is used trait, traitv2, traitv3 
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
+ type is a string which explains the tables purpose. It's sole purpose is to save developers from the effort to determine which table has what attributes
  + general is not for a specific purpose. Any table which have a plain values and table attributes are tagged with general
  + branching is for tables requires extra action. It usually leads to another tables according to the result. It containes following attributes: values, desc, action
  + background is only used for step 3. It has following attributes: values, desc, package, morph, next
  * package is used when result is a package It has values and package as attributes. package is no different than table when using it. 
  * event is used when it's an event table. It has same attributes with general but table is a list of objects and every object has the attributes desc and effect
  * info is used for general system info. It's just used for plain key-value storage
+ values represent results of dice rolls. Result could be a number or a range between two numbers ex. *[1, 2, 3, 4, 5, [6, 10]]*
+ desc is a string explains what will happen for that result
+ package if a result gives player a package this attribute is used. Only used in steps 3, 6, 9
+ next in table\_name object means the next path for character Only used in step 3. If used in an object except the table\_name it means a roll has to be made in the table\_name which is in the value of next
+ morph is starting morph for character 
+ action means its'a branching table which tells how to continue. It has attributes like next, select, roll. Select means how many PP will the selected packages be and roll attribute is used if multiple rolls needed on the table designated in next
+ table is a generic column used store results of rolls from different tables. If it's a event table results will be objects with desc and effect attributes. Desc will explain what will happen to the character and effect how they will be effected from this. Will they gain a trait, new skill, lose money etc. 
```json
{
    "1": {
        "values": [1, 2, 3, 4, 5, 6, 7, 8, [9, 10]],
        "table": ["Brawler", "Dilettante", "Extrovert", "Inquisitive", "Researcher", "Survivor", "Techie", "Thrill Seeker", "Choose or Re-roll"]
    },
    "3": {
        "values": [[1, 6], [7, 9], 10],
        "desc": ["Wholesome Youth", "Split Youth", "Fractured Youth"],
        "action": [{"next": "3.1", "select": 3}, {"next": "3.1", "roll": 2, "select": 1}, {"next": "3.1", "roll": 3, "select": 1}]
    },
    "3.6": {
        "values": [1, [2, 3], [4, 6], [7, 10]],
        "desc": ["Pioneer dynasty", "Venusian colonist: privileged homesteader", "Venusian colony staff", "Mercurian slave labor"],
        "package": ["hyperelite scion", "fall evacuee enclaver", {"next": "3.10"}, "indenture"],
        "morph": ["exalt ", "splicer ", "", {"values": [[1, 7], [8, 10]], "table":["flat", "case"]}],
        "next": ["6.5", "6.6", "", "6.7"]
    },
    "6.2": {
        "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "package": ["academic", "activist", "bot jammer", "covert ops", "explorer", "genehacker", "hacker", "medic", "scientist", "techie"]
    },
"7": {
        "values": [[1, 20], [21, 22], [23, 24], [25, 26], [27, 28], [29, 30], [31, 32], [33, 34], [35, 36], [37, 38], [39, 40], [41, 42], [43, 44], [45, 46], [47, 48], [49, 50], [51, 52], [53, 54], [55, 56], [57, 58], [59, 60], [61, 62], [63, 64], [65, 66], [67, 68], [69, 70], [71, 72], [73, 74], [75, 76], [77, 78], [79, 80], [81, 82], [83, 84], [85, 86], [87, 88], [89, 90], [91, 92], [93, 94], [95, 96], [97, 98], [99, 100]],
        "table": [
            {"desc": "Gain +1 Moxie and roll on the Story Event table ", "effect": {"moxie": 1, "next": "16"}},
            {"desc": "You save an animal from danger. Gain the Animal Empathy trait ).", "effect": {"trait": "animal empathy"}},
            {"desc": "You take up a sport. +10 to Climbing, Fray, Free Fall, Freerunning, or Swimming.", "effect": {"skills": {"fray": 10}}},
            {"desc": "Your inability to improve holds you back from an important promotion/advancement. Gain the Slow Learner trait ).", "effect": {"trait": "slow learner"}},
            {"desc": "You simply are not very comfortable with that whole resleeving thing. Gain the Morphing Disorder (Level 1) trait ).", "effect": {"trait": "morphing disorder"}},
            {"desc": "You are not a slacker. You take on part-time jobs or additional training. +20 to one skill.", "effect": {"skills": {"any": 20}}},
            {"desc": "You travel extensively. +10 to two different Language skills.", "effect": {"skills": {"language": [10, 10]}}},
        ]
    },
}
```

##Contributing
If you want to contribute or just report bugs feel free to send a pull request or open a issue.  
You can also drop me an email at ugurcanergn@gmail.com
##License and Attribution
Distributed with one of the argonauts favorite licenses GNU GPLv2  
Eclipse Phase is a trademark of Posthuman Studios LLC
