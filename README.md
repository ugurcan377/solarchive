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
+ "aptitude" is an object which has described before
+ "rep" is a number. "rep" denotes a network of players choice. If it was a specific network it will be "@-rep" for example
+ "moxie" and "credits" are numbers
+ "trait" is an array of strings
+ "psi" is either a number or an object. If it's a number, player can select this number of sleights regardless of sleights type, and it's an object it tells the player how many sleights of which type they can choose. Exp. *"psi": {"chi": 3, "gamma": 3}*
+ "skills" is an object it contains the name of skill as key and a number, array or object as value. The skills which does not have different fields are always represented with numbers. Skills that does have different fields are represented by either a number or an object. A number means player chooses the field and an object means a pre-selected specific field. If the skill value is an array this means multiple fields on that same skill.
```json
{
    "skills": {
        "free fall": 30, // "Skill without fields"
        "networking": 30, // "Skill with fields which one is players choice"
        "networking": {"value": 40, "spec": "scientists"}, // "A specific field"
        "academics": [40, 30], // "Skill with multiple fields"
        "profession": [ // "Skill with multiple specific fields"
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

##License and Attribution
Distributed with one of the argonauts favorite licenses GNU GPLv2  
Eclipse Phase is a trademark of Posthuman Studios LLC
