from models import Prize, Laureate, Country
import re

def searchTermAnd(term):
    links = []
    contexts = []
    titles = []
    terms = term.split(" ")

    prizes = Prize.query.filter_by().all()
    for prize in prizes:
        searchString = prize.category.capitalize()
        searchString += " Year: " + str(prize.year)
        searchString += " Number of Laureate: " + str(prize.nr_laureates)
        searchString += " Laureate:"
        for laureate in prize.laureates[:-1]:
            searchString += " " + laureate.name+","
        searchString += " " + prize.laureates[-1].name
        searchString += " Motivation: " + prize.motivation
        
        inString = True
        for query in terms:
            if query.lower() not in searchString.lower():
                inString = False
        #match = re.search("([^ ]*)"+term+"([^ ]*)", searchString, re.IGNORECASE)
        if inString:
            links += [prize.url]
            titles += [prize.category.capitalize() + ": " + str(prize.year)]
            contexts += [searchString]

    laureates = Laureate.query.filter_by().all()
    for laureate in laureates:
        searchString = laureate.name
        searchString += " Number of Prizes: " + str(laureate.nr_prizes)
        searchString += " Prizes:"
        laureatePrizes = laureate.prizes.all()
        for prize in laureatePrizes[:-1]:
            searchString += " " + prize.category + ": " + str(prize.year) + ","
        lastPrize = laureatePrizes[-1]
        searchString += " " + lastPrize.category + ": " + str(lastPrize.year) 
        searchString += " Year: " + str(laureatePrizes[0].year)
        searchString += " Gender: " + laureate.gender
        searchString += " Date of Birth: " + laureate.date_of_birth
        if laureate.country_id == None:
            searchString += " Country: N/A "
        else:        
            country = Country.query.get(laureate.country_id)
            searchString += " Country: " + country.name
        
        inString = True
        for query in terms:
            if query.lower() not in searchString.lower():
                inString = False
        #match = re.search("([^ ]*)"+term+"([^ ]*)", searchString, re.IGNORECASE)
        if inString:
            links += [laureate.url]
            titles += [laureate.name]
            contexts += [searchString]

    countries = Country.query.filter_by().all()
    for country in countries:
        searchString = country.name
        searchString += " Country Code: " + country.country_code
        searchString += " Population: " + str(country.population)
        searchString += " Number of Laureate: " + str(country.nr_laureates)
        searchString += " Number of Prizes: " + str(country.nr_prizes)
        
        inString = True
        for query in terms:
            if query.lower() not in searchString.lower():
                inString = False
        #match = re.search("([^ ]*)"+term+"([^ ]*)", searchString, re.IGNORECASE)
        if inString:
            links += [country.url]
            titles += [country.name]
            contexts += [searchString]
    
    return (links, titles, contexts)

if __name__ == "__main__" :
    print(searchTermAnd("taiwan"))
