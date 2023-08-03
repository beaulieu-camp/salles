import requests
import datetime

with open("./url.csv") as file:
    salles = file.read().split("\n")

def to_date(char):
    year = int(char[0:4])
    month = int(char[4:6])
    day = int(char[6:8])
    hour = int(char[9:11])
    minute = int(char[11:13])
    sec = int(char[13:15])
    date = datetime.datetime(year, month, day, hour, minute, sec)
    return int(date.timestamp())

salles_liste = []

for item in salles :
    if item == "" : break

    batiment,salle,url = item.split(",")
    salle_code = batiment.replace(" ","_") + "_" + salle.replace(" ","_")

    salles_liste.append([batiment,salle,salle_code])

    req = requests.get(url)

    liste = []

    DTSTART=""
    DTEND=""
    SUMMARY=""

    for item in req.text.split("\n"):
        line = item.split(":")
        code = line[0]
        value = ":".join(line[1:])

        if code == "DTSTART":
            DTSTART=to_date(value)
        elif code == "DTEND":
            DTEND=to_date(value)
        elif code == "SUMMARY":
            SUMMARY=value
        elif code == "END" and value == "VEVENT":
            liste.append([DTSTART , DTEND , SUMMARY])

    liste.sort()
    with open("./out/"+salle_code+".json","w+") as file:
        file.write(str(liste))

with open("./out/salles.json","w+") as file:
    file.write(str(salles_liste))