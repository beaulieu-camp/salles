import requests
import datetime
import json
import re

regex = re.compile( r"[A-z](.*) - (([A-z]?[-0-9]+)|([A-zÀ-ÿ ]*))" )

def to_date(char):
    year = int(char[0:4])
    month = int(char[4:6])
    day = int(char[6:8])
    hour = int(char[9:11])
    minute = int(char[11:13])
    sec = int(char[13:15])
    date = datetime.datetime(year, month, day, hour, minute, sec)
    return int(date.timestamp())

def formatKey(key):
    liste = key.split(" - ")
    print(key)
    try:
        matches = regex.findall(key)[0]
    except:
        return "unknown_building"
    bat = matches[0]
    code = "Salle"
    salle = matches[1]

    if salle.startswith("Hall "):
        code = "Hall"
        salle = salle.replace("Hall ","").lower()
    elif salle.startswith("Amphi "):
        code = "Amphi"
        salle = salle.replace("Amphi ","").lower()

    salle = "_".join(k for k in salle.split(" ") if k != "")

    return "Bâtiment_" + bat + "_" + code + "_" + salle

def batimentSupported(key) : 
    liste = ["41","42","02B"]
    return key.split("_")[1] in liste

salles_liste = {}

url = "https://planning.univ-rennes1.fr/jsp/custom/modules/plannings/KYND2kWv.shu"

req = requests.get(url)
if req.status_code != 200 : raise Exception("Api Univ Pété") 

liste = {}

DTSTART=""
DTEND=""
SUMMARY=""
LOCATIONS=""

text = req.text
text = text.replace("\r","")
text = text.replace("\n ","")
text = text.split("\n")


for item in text:
    line = item.split(":")
    code = line[0]
    value = ":".join(line[1:])

    if code == "DTSTART":
        DTSTART=to_date(value)
    elif code == "DTEND":
        DTEND=to_date(value)
    elif code == "LOCATION":
        LOCATIONS=value
    elif code == "SUMMARY":
        SUMMARY=value

    elif code == "END" and value == "VEVENT":
        for loc in LOCATIONS.split("\,"):

            LOCATION = formatKey(loc)

            if ( not batimentSupported(LOCATION) ) :
                continue


            if LOCATION not in liste:
                liste[LOCATION] = []
            liste[LOCATION].append([DTSTART , DTEND , SUMMARY])

with open("./out/salles.json","w+") as file:
    keyDic = {}
    for key in liste.keys():
        val = key.split("_")
        keyDic[key] = {
            "batiment":" ".join(val[0:2]),
            "salle":" ".join(val[2:])
        }
    file.write(json.dumps(keyDic))

for key,value in liste.items() :
    value.sort()
    with open("./out/"+key+".json","w+") as file:

        file.write(json.dumps(value))
