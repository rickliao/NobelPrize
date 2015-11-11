#!flask/bin/python
from db import db
from models import Prize, Laureate, Country
import requests
import json

db.drop_all()
db.create_all()
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

                     countryModel.nr_laureates += 1
                     countryModel.nr_prizes += 1
                     db.session.commit()
                     laureateModel = Laureate(personName, 1, person["born"], person["gender"], "/laureates/"+personName.replace(" ","_"), countryCode)
                     
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

# insert search text
prizes = Prize.query.filter_by().all()
for prize in prizes:
    searchString = " " + prize.category.capitalize()
    searchString += " Year: " + str(prize.year)
    searchString += " Number of Laureate: " + str(prize.nr_laureates)
    searchString += " Laureate:"
    for laureate in prize.laureates[:-1]:
        searchString += " " + laureate.name+","
    searchString += " " + prize.laureates[-1].name
    searchString += " Motivation: " + prize.motivation + " "
    
    prize.search_text = searchString

laureates = Laureate.query.filter_by().all()
for laureate in laureates:
    searchString = " " + laureate.name
    searchString += " Number of Prizes: " + str(laureate.nr_prizes)
    searchString += " Prizes:"
    laureatePrizes = laureate.prizes.all()
    for prize in laureatePrizes[:-1]:
        searchString += " " + prize.category + ": " + str(prize.year) + ","
    lastPrize = laureatePrizes[-1]
    searchString += " " + lastPrize.category + ": " + str(lastPrize.year)
    searchString += " Year: " + str(laureatePrizes[0].year)
    searchString += " Gender: " + laureate.gender
    searchString += " Date of Birth: " + laureate.date_of_birth
    if laureate.country_id == None:
        searchString += " Country: N/A "
    else:
        country = Country.query.get(laureate.country_id)
        searchString += " Country: " + country.name + " "

    laureate.search_text = searchString

countries = Country.query.filter_by().all()
for country in countries:
    searchString = " " + country.name
    searchString += " Country Code: " + country.country_code
    searchString += " Population: " + str(country.population)
    searchString += " Number of Laureate: " + str(country.nr_laureates)
    searchString += " Number of Prizes: " + str(country.nr_prizes) + " "

    country.search_text = searchString

db.session.commit()
