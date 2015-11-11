from models import Prize, Laureate, Country
import re

def searchTerm(term):
    links = []
    contexts = []
    title = []

    prizes = Prize.query.filter_by().all()
    for prize in prizes:
        searchString = " " + prize.category.capitalize()
        searchString += " Year: " + str(prize.year)
        searchString += " Number of Laureate: " + str(prize.nr_laureates)
        searchString += " Laureate:"
        for laureate in prize.laureates[:-1]:
            searchString += " " + laureate.name+","
        searchString += " " + prize.laureates[-1].name
        searchString += " Motivation: " + prize.motivation + " "
        
        match = re.search("([^ ]*) "+term+" ([^ ]*)", searchString, re.IGNORECASE)
        if match != None:
            links += [prize.url]
            title += [prize.category.capitalize() + ": " + str(prize.year)]
            contexts += [match.group(0)]

    laureates = Laureate.query.filter_by().all()
    for laureate in laureates:
        searchString = " " + laureate.name
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
            searchString += " Country: " + country.name + " "
 
        match = re.search("([^ ]*) "+term+" ([^ ]*)", searchString, re.IGNORECASE)
        if match != None:
            links += [laureate.url]
            title += [laureate.name]
            contexts += [match.group(0)]

    countries = Country.query.filter_by().all()
    for country in countries:
        searchString = " " + country.name
        searchString += " Country Code: " + country.country_code
        searchString += " Population: " + str(country.population)
        searchString += " Number of Laureate: " + str(country.nr_laureates)
        searchString += " Number of Prizes: " + str(country.nr_prizes) + " "
        
        match = re.search("([^ ]*) "+term+" ([^ ]*)", searchString, re.IGNORECASE)
        if match != None:
            links += [country.url]
            title += [country.name]
            contexts += [match.group(0)]
    print(links)
    print(title)
    print(contexts)

if __name__ == "__main__" :
    searchTerm("2013")
