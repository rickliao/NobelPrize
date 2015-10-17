from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

prize_rows = dict()
prize_rows[1] = dict(url='/2008/economics', numLaureate=1, year=2008, category='Economics', motivation='\"for his analysis of trade patterns and location of economic activity\"', laureate=['Paul Krugman'])
prize_rows[2] = dict(url='/2015/physics', numLaureate=2, year=2015, category='Physics', motivation='\"for the discovery of neutrino oscillations, which shows that neutrinos have mass\"', laureate=['Takaaki Kajita', 'Arthur B. McDonald'])
prize_rows[3] = dict(url='/1964/chemistry', numLaureate=1, year=1964, category='Chemistry', motivation='\"for her determinations by X-ray techniques of the structures of important biochemical substances\"', laureate=['Dorothy Crowfoot Hodgkin'])

@app.route("/prize")
def render_prize():
    return render_template('prize.html', entries = prize_rows)

@app.route("/2008/economics")
def render_2008_economics():
	return render_template('prize_template.html', entry = prize_rows[1])

@app.route("/2015/physics")
def render_2015_physics():
	return render_template('prize_template.html', entry = prize_rows[2])

@app.route("/1964/chemistry")
def render_1964_chemistry():
	return render_template('prize_template.html', entry = prize_rows[3])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
