from flask import render_template, abort
from db import db, app
from flask.ext.restless import APIManager
from models import Prize, Laureate, Country
import requests
import json
from urllib.parse import quote
import os
#from search_db import searchTerm

manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Prize, methods=['GET'], include_columns=['id', 'category', 'laureates', 'year', 'nr_laureates'])
manager.create_api(Laureate, methods=['GET'], include_columns=['id', 'name', 'country_id', 'date_of_birth', 'gender', 'nr_prizes'])
manager.create_api(Country, methods=['GET'], include_columns=['country_code', 'name', 'laureates', 'nr_laureates', 'nr_prizes', 'population'])

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/prize")
def render_prize():
    prizes = Prize.query.filter_by().all()
    return render_template('prize_db.html', prizes = prizes)

@app.route("/laureates")
def render_laureate():
    laureates = Laureate.query.filter_by().all()
    entries = []
    for laureate in laureates:
        prizes = laureate.prizes.all()
        prizesList = []
        prizesUrlList = []
        for prize in prizes:
            prizeName = prize.category+": "+str(prize.year)
            prizesList += [prizeName]
            prizesUrlList += [prize.url]

        if not (laureate.country_id == None):
            country = Country.query.get(laureate.country_id)
            countryName = country.name
            countryUrl = country.url
        else:
           countryName = "N/A"
           countryUrl = "/error"
        
        entry = {'url':laureate.url, 'id':laureate.id, 'name':laureate.name, 'numPrizes':laureate.nr_prizes, 'prizes':prizesList, 'prizesUrl':prizesUrlList, 'dob':laureate.date_of_birth, 'gender':laureate.gender, 'country':countryName, 'countryUrl':countryUrl}
        entries += [entry]

    return render_template('laureate_db.html', entries = entries)

@app.route("/countries")
def render_countries():
    countries = Country.query.filter_by().all()
    return render_template('country_db.html', countries = countries)


@app.route("/prizes/<myYear>/<myCategory>")
def render_individual_prize(myYear, myCategory):
    prize = Prize.query.filter_by(year = myYear, category = myCategory).first()
    if prize == None:
        abort(404)

    laureates = prize.laureates
    laureateNames = []
    laureateUrls = []
    for laureate in laureates:
        laureateNames += [laureate.name]
        laureateUrls += [laureate.url]
    entry = {'year':prize.year, 'category':prize.category.capitalize(), 'motivation':prize.motivation, 'numLaureate':len(laureateNames), 'laureate':laureateNames, 'laureateUrl':laureateUrls}

    # embed image
    search = "nobel prize "+str(prize.year)+" "+prize.category
    url, width, height = getImage(search)

    return render_template('prize_template.html', entry = entry, imageUrl = url, width = width, height = height)

@app.route("/laureates/<myName>")
def render_individual_laureate(myName):
    laureate = Laureate.query.filter_by(name=myName.replace("_"," ")).first()
    if laureate == None:
        abort(404)
    
    prizes = laureate.prizes.all()
    prizesList = []
    prizesUrlList = []
    year = 0 
    for prize in prizes:
        prizeName = prize.category+": "+str(prize.year)
        prizesList += [prizeName]
        prizesUrlList += [prize.url]
        year = prize.year

    if not (laureate.country_id == None):
        country = Country.query.get(laureate.country_id)
        countryName = country.name
        countryUrl = country.url
    else:
        countryName = "N/A"
        countryUrl = "/error"

    entry = {'name':laureate.name, 'year':year, 'numPrizes':laureate.nr_prizes, 'prizes':prizesList, 'prizesUrl':prizesUrlList, 'dob':laureate.date_of_birth, 'gender':laureate.gender, 'country':countryName, 'countryUrl':countryUrl}

    # embed image
    url, width, height = getImage(laureate.name)

    return render_template('laureate_template.html', entry = entry, imageUrl = url, width = width, height = height)

@app.route("/countries/<myName>")
def render_individual_countries(myName):
    country = Country.query.filter_by(name = myName.replace("_", " ")).first()
    if country == None:
        abort(404)

    entry = {'name':country.name, 'code':country.country_code, 'numLaureates':country.nr_laureates, 'numPrizes':country.nr_prizes, 'pop':country.population}

    # embed image
    url, width, height = getImage(country.name)

    return render_template('country_template.html', entry = entry, imageUrl = url, width = width, height = height)

@app.route("/about")
def render_about():
    return render_template('about.html');

def getImage(query):
    # embed image
    response = requests.get("https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="+quote(query))
    result = json.loads(response.text)
   
    # scale image 
    firstResult = result['responseData']['results'][0]
    width = int(firstResult['width'])
    height = int(firstResult['height'])
    while width > 500 or height > 500:
        width /= 2
        height /= 2

    print(width, height)
    return (firstResult['url'], width, height)

@app.route("/aboutT")
def test_link():
    os.system("make test")
    f = open("TestModels.tmp", 'r')
    result = []
    for line in f:
        result += [line]
    f.close()
    os.system("make clean")    
    return render_template('aboutT.html', result=result);

@app.route("/search/<query>")
def render_search(query):
    return str(query);

@app.errorhandler(404)
def error_404(error):
    return render_template('error.html'), 404

@app.route("/error")
def error():
    return render_template('error.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
