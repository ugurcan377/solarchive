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
+ trait is an array of strings
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
+ values represent results of dice rolls. Result could be a number or a range between two numbers ex. *[1, 2, 3, 4, 5, [6, 10]]*
+ desc is a string explains what will happen for that result
+ package if a result gives player a package this attribute is used. Only used in steps 3, 6, 9
+ next in table\_name object means the next path for character Only used in step 3. If used in an object except the table\_name it means a roll has to be made in the table\_name which is in the value of next
+ morph is starting morph for character 
+ action means its'a branching table which tells how to continue. It has attributes like next, select, roll. Select means how many PP will the selected packages be and roll attribute is used if multiple rolls needed on the table designated in next
+ table is a generic column used store results of rolls from different tables. If it's a event table results will be objects with desc and effect attributes. Desc will explain what will happen to the character and effect how they will be effected from this. Will they gain a trait, new skill, lose money etc. 

##License and Attribution
Distributed with one of the argonauts favorite licenses GNU GPLv2  
Eclipse Phase is a trademark of Posthuman Studios LLC
