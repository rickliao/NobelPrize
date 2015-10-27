#!flask/bin/python
from app import db
from models import Prize
#from sqlalchemy import create_engine

#eng = create_engine(db.app.config['SQLALCHEMY_DATABASE_URI'])
db.create_all()
prize= Prize("Pysics", 1991, 2, "motivation1")
db.session.add(prize)
db.session.commit()
