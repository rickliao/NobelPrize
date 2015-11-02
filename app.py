from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://nobeladmin:cs373Prize@localhost/nobeldb'
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template('index.html')

prize_rows = dict()
# dict key = id
prize_rows[1] = dict(url='/2008/economics', numLaureate=1, year=2008, category='Economics', motivation='\"for his analysis of trade patterns and location of economic activity\"', laureate=['Paul Krugman'], laureateUrl=['/laureates/paul_krugman'])
prize_rows[2] = dict(url='/2015/physics', numLaureate=2, year=2015, category='Physics', motivation='\"for the discovery of neutrino oscillations, which shows that neutrinos have mass\"', laureate=['Takaaki Kajita'], laureateUrl=['/laureates/takaaki_kajita'])
prize_rows[3] = dict(url='/1964/chemistry', numLaureate=1, year=1964, category='Chemistry', motivation='\"for her determinations by X-ray techniques of the structures of important biochemical substances\"', laureate=['Dorothy Crowfoot Hodgkin'], laureateUrl=['/laureates/dorothy_crowfoot_hodgkin'])

laureate_rows = dict()
#dict key = id
laureate_rows[230] = dict(url='/laureates/dorothy_crowfoot_hodgkin', name='Dorothy Crowfoot Hodgkin', year=1964, numPrizes=1, dob='1910-05-12', gender='F', country='UK', countryUrl='/countries/unitedkingdom', prizes=['Chemistry: 1964'], prizesUrl=['/1964/chemistry'])
laureate_rows[834] = dict(url='/laureates/paul_krugman', name='Paul Krugman', year=2008, numPrizes=1, dob='1953-02-28', gender='M', country='US', countryUrl='/countries/unitedstates', prizes=['Economics: 2008'], prizesUrl=['/2008/economics'])
laureate_rows[919] = dict(url='/laureates/takaaki_kajita', name='Takaaki Kajita', year=2015, numPrizes=1, dob='0000-00-00', gender='M', country='JP', countryUrl='/countries/japan', prizes=['Physics: 2015'], prizesUrl=['/2015/physics'])

country_rows = dict()
#dict key = id
# country_rows[1] = dict(url='/countries/afghanistan', code='AF', name='Afghanistan', numPrizes=0, numLaureates=0, pop=26023100)
country_rows[1] = dict(url='/countries/unitedstates', code= 'US',  name='United States', numPrizes=356, numLaureates=356, pop=321645000)
country_rows[2] = dict(url='/countries/unitedkingdom', code='UK', name='United Kingdom', numPrizes=116, numLaureates=116, pop=64800000)
country_rows[3] = dict(url='/countries/japan', code='JP', name='Japan', numPrizes=24, numLaureates=24, pop=126865000)

@app.route("/prize")
def render_prize():
    return render_template('prize.html', entries = prize_rows)

@app.route("/2008/economics")
def render_2008_economics():
	return render_template('economics_2008.html', entry = prize_rows[1])

@app.route("/2015/physics")
def render_2015_physics():
	return render_template('physics_2015.html', entry = prize_rows[2])

@app.route("/1964/chemistry")
def render_1964_chemistry():
	return render_template('chemistry_1964.html', entry = prize_rows[3])

@app.route("/countries")
def render_countries():
	return render_template('country.html', entries = country_rows)

@app.route("/countries/unitedkingdom")
def render_unitedkingdom():
	return render_template('unitedkingdom.html', entry = country_rows[2])

@app.route("/countries/unitedstates")
def render_unitedstates():
	return render_template('unitedstates.html', entry = country_rows[1])

@app.route("/countries/japan")
def render_japan():
	return render_template('japan.html', entry = country_rows[3])

@app.route("/laureates")
def render_laurates():
	return render_template('laureate.html', entries = laureate_rows)

@app.route("/laureates/paul_krugman")
def render_paul_krugman():
	return render_template('paul_krugman.html', entry = laureate_rows[834])

@app.route("/laureates/takaaki_kajita")
def render_takaaki_kajita():
	return render_template('takaaki_kajita.html', entry = laureate_rows[919])

@app.route("/laureates/arthur_mcdonald")
def render_arthur_mcdonald():
	return "Haven't made the page, only three instances of laureates required";

@app.route("/laureates/dorothy_crowfoot_hodgkin")
def render_dorothy_crowfoot_hodgkin():
	return render_template('dorothy_crowfoot_hodgkin.html', entry = laureate_rows[230])

@app.route("/about")
def render_about():
	return render_template('about.html');

@app.route("/aboutT/")
def test_link():
	print ('my test fun works')
	os.system("make test")
	return 'hi'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
