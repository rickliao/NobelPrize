from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://nobeladmin:cs373Prize@localhost/nobeldb'
db = SQLAlchemy(app)
