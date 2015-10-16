from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/prize")
def test():
    rows = []
    rows += [dict(id=1, numLaureate=10, year=2015, category='physics', motivation='hello')]
    return render_template('prize.html', entries = rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
