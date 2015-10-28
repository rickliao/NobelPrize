#!flask/bin/python
from app import db
from models import Prize, Laureate, Country
import requests
import json

#db.create_all()
response = requests.get("http://api.nobelprize.org/v1/prize.json")
if response.ok:
    all = json.loads(response.text)
    
    for prize in all["prizes"] :
        laureates = prize["laureates"]
        try:
            prizeModel = Prize(prize["category"], prize["year"], len(laureates), laureates[0]["motivation"], "/"+prize["year"]+"/"+prize["category"])
        except KeyError:
            print("KeyError on "+prize["year"]+" "+prize["category"])
            prizeModel = Prize(prize["category"], prize["year"], len(laureates), "", "/"+prize["year"]+"/"+prize["category"])
        

        for laureate in laureates :
            laureateResponse = requests.get("http://api.nobelprize.org/v1/laureate.json?id="+laureate["id"])
            person = json.loads(laureateResponse.text)["laureates"][0] #only one returns
            if "firstname" in person and "surname" in person:
                personName = person["firstname"]+" "+person["surname"]
            elif "firstname" in person :
                personName = person["firstname"]
            else:
                personName = person["surname"]

            if Laureate.query.filter_by(name = personName).first() == None :
                 if "bornCountryCode" in person :
                     countryCode = person["bornCountryCode"]
                     countryModel = Country.query.filter_by(country_code = countryCode).first()

                     if countryModel == None :
                         countryResponse = requests.get("https://restcountries.eu/rest/v1/alpha?codes="+countryCode)
                         if countryResponse.ok:
                             country = json.loads(countryResponse.text)[0] #again only one item
                             countryModel = Country(countryCode, country["name"], 0, 0, country["population"], "/countries/"+country["name"].replace(" ", "_"))
                             db.session.add(countryModel)
              
                     countryId = countryModel.id
                     
                     laureateModel = Laureate(personName, 1, person["born"], person["gender"], "/laureates/"+personName.replace(" ","_"), countryId)
                 else:
                     laureateModel = Laureate(personName, 1, person["born"], person["gender"], "/laureates/"+personName.replace(" ","_"), None)
                 db.session.add(laureateModel)



db.session.commit()
