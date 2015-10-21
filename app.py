from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

prize_rows = dict()
# dict key = id
prize_rows[1] = dict(url='/2008/economics', numLaureate=1, year=2008, category='Economics', motivation='\"for his analysis of trade patterns and location of economic activity\"', laureate=['Paul Krugman'])
prize_rows[2] = dict(url='/2015/physics', numLaureate=2, year=2015, category='Physics', motivation='\"for the discovery of neutrino oscillations, which shows that neutrinos have mass\"', laureate=['Takaaki Kajita', 'Arthur B. McDonald'])
prize_rows[3] = dict(url='/1964/chemistry', numLaureate=1, year=1964, category='Chemistry', motivation='\"for her determinations by X-ray techniques of the structures of important biochemical substances\"', laureate=['Dorothy Crowfoot Hodgkin'])

laureate_rows = dict()
#dict key = id
laureate_rows[230] = dict(url='/laureates/dorothy_crowfoot_hodgkin', name='Dorothy Crowfoot Hodgkin', year=1964, prizes=1, dob='1910-05-12', gender='F')
laureate_rows[834] = dict(url='/laureates/paul_krugman', name='Paul Krugman', year=2008, prizes=1, dob='1953-02-28', gender='M')
laureate_rows[919] = dict(url='/laureates/takaaki_kajita', name='Takaaki Kajita', year=2015, prizes=1, dob='0000-00-00', gender='M')

country_rows = dict()
#dict key = id
country_rows[1] = dict(url='/countries/afghanistan', name='Afghanistan', numPrizes=0, numLaureates=0, pop=26023100)
country_rows[2] = dict(url='/countries/unitedstates', name='United States', numPrizes=356, numLaureates=356, pop=321645000)
country_rows[3] = dict(url='/countries/unitedkingdom', name='United Kingdom', numPrizes=116, numLaureates=116, pop=64800000)

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
	return render_template('unitedkingdom.html', entry = country_rows[3])

@app.route("/countries/unitedstates")
def render_unitedstates():
	return render_template('unitedstates.html', entry = country_rows[2])

@app.route("/countries/afghanistan")
def render_afghanistan():
	return render_template('afghanistan.html', entry = country_rows[1])

@app.route("/laureates")
def render_laurates():
	return render_template('laureate.html', entries = laureate_rows)

@app.route("/laureates/dorothy_crowfoot_hodgkin")
def render_dorothy_crowfoot_hodgkin():
	return render_template('laureate_template.html', entry = laureate_rows[230])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
