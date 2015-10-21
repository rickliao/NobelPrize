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

laurate_rows = dict()
#dict key = id
laurate_rows[1] = dict(url='wilhelm/röntgen', id=1, name='Wilhelm Röntgen', year=1901, prizes=1, dob='1845-03-27', gender='M')
laurate_rows[1] = dict(url='hendrik/lorentz', id=2, name='Hendrik Lorentz', year=1902, prizes=1, dob='1853-07-18', gender='M')
laurate_rows[1] = dict(url='pieter/zeeman', id=3, name='Pieter Zeeman', year=1902, prizes=1, dob='1865-05-25', gender='M')

country_rows = dict()
#dict key = id
country_rows[1] = dict(url='countries/Afghanistan', id=1, name='Afghanistan', numPrizes=0, numLaureates=0, pop=26023100)
country_rows[1] = dict(url='countries/unitedstates', id=2, name='United States', numPrizes=356, numLaureates=356, pop=321645000)
country_rows[1] = dict(url='countries/unitedkingdom', id=3, name='United Kingdom', numPrizes=116, numLaureates=116, pop=64800000)

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

@app.route("countries")
def render_countries():
	return render_template('country_template.html' entry = country_rows[3])

@app.route("laurate")
def render_laurates():
	return render_template('laureate_template')
if __name__ == "__main__":
    app.run(host='0.0.0.0')
