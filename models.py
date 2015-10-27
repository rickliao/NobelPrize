from app import db

"""
Additional table to map the many to many relationship between Prize and Laureate
Maps laureate id to prize id, with the values being a foreign key representing
the id attribute in each table
"""
laureates = db.Table('tags',
    db.Column('laureate_id', db.Integer, db.ForeignKey('laureate.id')),
    db.Column('prize_id', db.Integer, db.ForeignKey('prize.id'))
)

"""
Class representing the Prize table
Class variables are columns
Each instance of this class is a row
"""
class Prize(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80))
    year = db.Column(db.Integer)
    nr_laureates = db.Column(db.Integer)
    motivation = db.Column(db.String(250))
    
    #Many to many relationship
    laureates = db.relationship('Laureate', secondary=laureates,
            backref=db.backref('prizes', lazy='dynamic'))

    # Constructor
    def __init__(self, category, year, nr_laureates, motivation):
        self.category = category
        self.year = year
        self.nr_laureates = nr_laureates
        self.motivation = motivation

    def __repr__(self):
        return '<Prize %r>' % self.category


"""
Class representing the Laureate table
Class variables are columns
Each instance of this class is a row
"""
class Laureate(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    nr_prizes = db.Column(db.Integer)
    date_of_birth = db.Column(db.DateTime)
    gender = db.Column(db.String(1))
    
    #One to many relationship
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))

    #Constructor
    def __init__(self, name, nr_prizes, date_of_birth, gender) :
        self.name = name
        self.nr_prizes = nr_prizes
        self.date_of_birth = date_of_birth
        self.gender = gender
    
    def __repr__(self) :
        return '<Laureate %r>' % self.name

"""
Class representing the Country table
Class variables are columns
Each instance of this class is a row
"""
class Country(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(2))
    name = name = db.Column(db.String(80))
    nr_laureates = db.Column(db.Integer)
    nr_prizes = db.Column(db.Integer)
    population = db.Column(db.Integer)
    
    #One to many relationship
    laureates = db.relationship('Laureate', backref='country', lazy='dynamic')
    
    #Constructor
    def __init__(self, country_code, name, nr_laureates, nr_prizes, population) :
        self.country_code = country_code
        self.name = name
        self.nr_laureates = nr_laureates
        self.nr_prizes = nr_prizes
        self.population = population

    def __repr__(self) :
        return '<Country %r>' % self.name
