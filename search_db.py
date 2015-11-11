from models import Prize, Laureate, Country
import re

def searchTermAnd(term):
    links = []
    contexts = []
    titles = []
    terms = term.split(" ")

    prizes = Prize.query.filter_by().all()
    for prize in prizes:
        searchString = prize.search_text 
        #match = re.search("([^ ]*)"+term+"([^ ]*)", searchString, re.IGNORECASE)
        if allInString(terms, searchString):
            links += [prize.url]
            titles += [prize.category.capitalize() + ": " + str(prize.year)]
            contexts += [searchString]

    laureates = Laureate.query.filter_by().all()
    for laureate in laureates:
        searchString = laureate.search_text 
        #match = re.search("([^ ]*)"+term+"([^ ]*)", searchString, re.IGNORECASE)
        if allInString(terms, searchString):
            links += [laureate.url]
            titles += [laureate.name]
            contexts += [searchString]

    countries = Country.query.filter_by().all()
    for country in countries:
        searchString = country.search_text 
        #match = re.search("([^ ]*)"+term+"([^ ]*)", searchString, re.IGNORECASE)
        if allInString(terms, searchString):
            links += [country.url]
            titles += [country.name]
            contexts += [searchString]
    
    return (links, titles, contexts)

def allInString(terms, searchString):
    inString = True
    for query in terms:
        if query.lower() not in searchString.lower():
            inString = False
    return inString


if __name__ == "__main__" :
    print(searchTermAnd("yuan taiwan"))
