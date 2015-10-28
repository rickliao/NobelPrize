#!flask/bin/python
from app import db
from models import Prize, Laureate, Country
import requests
import json

#db.create_all()
response = requests.get("http://api.nobelprize.org/v1/prize.json")
if response.ok:
    all = json.loads(response.text)
    
    # loop through all prizes
    for prize in all["prizes"] :
        laureates = prize["laureates"]
        try:
            prizeModel = Prize(prize["category"], prize["year"], len(laureates), laureates[0]["motivation"], "/prizes/"+prize["year"]+"/"+prize["category"])
        except KeyError:
            # has no motivation
            print("KeyError on "+prize["year"]+" "+prize["category"])
            prizeModel = Prize(prize["category"], prize["year"], len(laureates), "", "/"+prize["year"]+"/"+prize["category"])
        
        # loop through each laureate of the prize
        for laureate in laureates :
            laureateResponse = requests.get("http://api.nobelprize.org/v1/laureate.json?id="+laureate["id"])
            person = json.loads(laureateResponse.text)["laureates"][0] #only one returns
            if "firstname" in person and "surname" in person:
                personName = person["firstname"]+" "+person["surname"]
            elif "firstname" in person :
                personName = person["firstname"]
            else:
                personName = person["surname"]

            # if laureate didn't already exist
            if Laureate.query.filter_by(name = personName).first() == None :
                 if "bornCountryCode" in person :
                     countryCode = person["bornCountryCode"]
                     countryModel = Country.query.filter_by(country_code = countryCode).first()

                     # if country didn't already exist
                     if countryModel == None :
                         countryResponse = requests.get("https://restcountries.eu/rest/v1/alpha?codes="+countryCode)
                         if countryResponse.ok:
                             country = json.loads(countryResponse.text)[0] #again only one item
                             countryModel = Country(countryCode, country["name"], 0, 0, country["population"], "/countries/"+country["name"].replace(" ", "_"))
                             db.session.add(countryModel)
                             print(countryModel)
                             db.session.commit()

                     countryId = countryModel.id
                     countryModel.nr_laureates += 1
                     countryModel.nr_prizes += 1
                     db.session.commit()
                     laureateModel = Laureate(personName, 1, person["born"], person["gender"], "/laureates/"+personName.replace(" ","_"), countryId)
                     
                 else:
                     laureateModel = Laureate(personName, 1, person["born"], person["gender"], "/laureates/"+personName.replace(" ","_"), None)
                 print(laureateModel)
                 db.session.add(laureateModel)
            else:
                 # increment # prize for laureate and country if already exist
                 laureateModel = Laureate.query.filter_by(name = personName).first()
                 laureateModel.nr_prizes = laureateModel.nr_prizes + 1
                 if laureateModel.country_id != None :
                     c = Country.query.get(laureateModel.country_id)
                     c.nr_prizes += 1

            prizeModel.laureates.append(laureateModel)
            db.session.commit()
    
        print(prizeModel)
        db.session.add(prizeModel)
        db.session.commit()
