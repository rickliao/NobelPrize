from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models import Prize, Laureate, Country

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://nobeladmin:cs373Prize@localhost/nobeldb'
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/prizes/<myYear>/<myCategory>")
def render_individual_prize(myYear, myCategory):
    prize = Prize.query.filter_by(year = myYear, category = myCategory).first()
    if prize == None:
        return "no such prize, dummy"
    laureates = prize.laureates
    laureateNames = []
    laureateUrls = []
    for laureate in laureates:
        laureateNames += [laureate.name]
        laureateUrls += [laureate.url]
    entry = {'year':prize.year, 'category':prize.category, 'motivation':prize.motivation, 'numLaureate':len(laureateNames), 'laureate':laureateNames, 'laureateUrl':laureateUrls}
    return render_template('prize_template.html', entry = entry)


@app.route("/about")
def render_about():
	return render_template('about.html');

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
