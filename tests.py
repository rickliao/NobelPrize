import unittest
from flask.ext.testing import TestCase

from db import db, app
from models import Prize, Laureate, Country
from search_db import searchTermAnd, searchTermOr

TEST_DATABASE_URI = "sqlite://"
#TEST_DATABASE_URI = 'mysql://nobeladmin:cs373Prize@localhost/nobeldb'

class TestPrizes(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()
        prize1 = Prize("Physics", 1991, 2, "motivation1", "u1")
        prize2 = Prize("Peace", 1950, 1, "motivation2", "u2")
        db.session.add(prize1)
        db.session.add(prize2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_prizes(self):
        prizes = Prize.query.all()
        assert len(prizes) == 2

    def test_repr(self):
        prize = Prize.query.filter_by(category="Physics", year=1991).first()
        assert repr(prize) == "<Prize Physics 1991>" 

    def test_filtering_prizes(self):   
        prize = Prize.query.filter_by(category = 'Physics').first()
        assert prize.year == 1991 and prize.motivation == "motivation1"

        prize = Prize.query.filter(Prize.year < 1991).first()
        assert prize.category == 'Peace' and prize.motivation == "motivation2"  

    def test_add_delete_prizes(self):
        prize3 = Prize("Physics", 2015, 4, "motivation3", "u3")
        db.session.add(prize3)
        db.session.commit()
        assert len(Prize.query.all()) == 3

        Prize.query.filter_by(category = 'Physics').delete()
        db.session.commit()
        assert len(Prize.query.all()) == 1 


class TestLaureates(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()
        laureate1 = Laureate("John Doe", 1, "1956-11-2", "M", "u1", 1)
        laureate2 = Laureate("Jane Doe", 2, "1939-4-7", "F", "u2", 1)
        db.session.add(laureate1)
        db.session.add(laureate2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_laureates(self):
        laureates = Laureate.query.all()
        assert len(laureates) == 2

    def test_repr(self):
        laureate = Laureate.query.filter_by(name="John Doe", gender="M").first()
        assert repr(laureate) == "<Laureate 'John Doe'>" 

    def test_filtering_laureates(self):   
        laureate = Laureate.query.filter_by(name = 'John Doe').first()
        assert laureate.nr_prizes == 1 and laureate.gender == "M"

        laureate = Laureate.query.filter(Laureate.nr_prizes > 1).first()
        assert laureate.name == 'Jane Doe' and laureate.gender == "F"  

    def test_add_delete_laureate(self):
        laureate3 = Laureate("Anne Smith", 1, "1890-1-1", "F", "u3", 1)
        db.session.add(laureate3)
        db.session.commit()
        assert len(Laureate.query.all()) == 3

        Laureate.query.filter_by(gender = 'F').delete()
        db.session.commit()
        assert len(Laureate.query.all()) == 1 


class TestCountries(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()
        country1 = Country("SE", "Sweden", 10, 7, 10000000, "u1")
        country2 = Country("US", "United States", 18, 10, 300000000, "u2")
        db.session.add(country1)
        db.session.add(country2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_countries(self):
        countries = Country.query.all()
        assert len(countries) == 2

    def test_repr(self):
        country = Country.query.filter_by(name="Sweden").first()
        assert repr(country) == "<Country 'Sweden'>" 

    def test_filtering_countries(self):   
        country = Country.query.filter_by(country_code = 'SE').first()
        assert country.name == 'Sweden' and country.nr_laureates == 10

        country = Country.query.filter(Country.population > 10000000).first()
        assert country.name == 'United States' and country.nr_laureates == 18

    def test_add_delete_country(self):
        country3 = Country("UK", "United Kingdom", 11, 7, 50000000, "u3")
        db.session.add(country3)
        db.session.commit()
        assert len(Country.query.all()) == 3

        Country.query.filter_by(nr_prizes = 7).delete()
        db.session.commit()
        assert len(Country.query.all()) == 1 


class TestSearch(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()
        laureate1 = Laureate("Yuan", 1, "1956-11-2", "M", "u1", 1)
        laureate1.search_text = "yuan taiwan"
        laureate2 = Laureate("Yuan", 2, "1939-4-7", "F", "u2", 1)
        laureate2.search_text = "yuan"
        prize1 = Prize("Physics", 1991, 2, "motivation1", "u1")
        prize1.search_text = "one yuan"
        prize2 = Prize("Physics", 1991, 2, "motivation1", "u1")
        prize2.search_text = "taiwan one yuan"
        country1 = Country("SE", "Sweden", 10, 7, 10000000, "u1")
        country1.search_text = "taiwan ldksfjsl;fkjsd yuan"
        country2 = Country("SR", "Sweden", 10, 7, 10000000, "u1")
        country2.search_text = "two yuan"
        db.session.add(laureate1)
        db.session.add(laureate2)
        db.session.add(prize1)
        db.session.add(prize2)
        db.session.add(country1)
        db.session.add(country2)
        db.session.commit()
  
    def tearDown(self):
        db.session.remove()
        db.drop_all()
 
    def test_search_and(self):
        links, titles, contexts = searchTermAnd("yuan taiwan")
        assert len(links) == len(titles)
        assert len(titles) == len(contexts)
        assert len(links) == 3

    def test_search_or(self):
        links, titles, contexts = searchTermOr("yuan taiwan")
        assert len(links) == len(titles)
        assert len(titles) == len(contexts)
        assert len(links) == 6

if __name__ == '__main__':
    unittest.main()
