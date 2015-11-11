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
        if allInString(terms, searchString):
            links += [prize.url]
            titles += [prize.category.capitalize() + ": " + str(prize.year)]
            contexts += [findContexts(terms, searchString)]

    laureates = Laureate.query.filter_by().all()
    for laureate in laureates:
        searchString = laureate.search_text 
        if allInString(terms, searchString):
            links += [laureate.url]
            titles += [laureate.name]
            contexts += [findContexts(terms, searchString)]

    countries = Country.query.filter_by().all()
    for country in countries:
        searchString = country.search_text 
        if allInString(terms, searchString):
            links += [country.url]
            titles += [country.name]
            contexts += [findContexts(terms, searchString)]
    
    return (links, titles, contexts)

def allInString(terms, searchString):
    inString = True
    for query in terms:
        if query.lower() not in searchString.lower():
            inString = False
    return inString

# also return a list of queries that exist in searchString
def oneInString(terms, searchString):
    inString = False
    inStringList = []
    for query in terms:
        if query.lower() in searchString.lower():
            inString = True
            inStringList += [query]
    return (inString, inStringList) 

def findContexts(terms, searchString):
    context = ""
    # find bound (inclusive, exclusive)
    min = len(searchString)
    max = -1
    for query in terms:
        i = searchString.lower().index(query.lower())
        if i < min:
            min = i
        if i+len(query) > max:
            max = i+len(query)
    words = re.compile("([.*] [.*] [.*]){0,3}")
    matchBeg = words.search(searchString, 0, min)
    matchEnd = words.search(searchString, max, len(searchString))
    print(matchBeg.group(0)+searchString[min:max]+matchEnd.group(0))
    for query in terms:
        if query not in context:
            match = re.search("(.{0,10})"+query+"(.{0,10})", searchString, re.IGNORECASE)
            if match != None:
                if "..." in context:
                    context += match.group(0)+"..."
                else:
                    context += "..."+match.group(0)+"..."
    return matchBeg.group(0)+searchString[min:max]+matchEnd.group(0)

def searchTermOr(term):
    links = []
    contexts = []
    titles = []
    terms = term.split(" ")

    prizes = Prize.query.filter_by().all()
    for prize in prizes:
        searchString = prize.search_text 
        inString, inStringList = oneInString(terms, searchString)
        if inString:
            links += [prize.url]
            titles += [prize.category.capitalize() + ": " + str(prize.year)]
            contexts += [findContexts(inStringList, searchString)]

    laureates = Laureate.query.filter_by().all()
    for laureate in laureates:
        searchString = laureate.search_text 
        inString, inStringList = oneInString(terms, searchString)
        if inString:
            links += [laureate.url]
            titles += [laureate.name]
            contexts += [findContexts(inStringList, searchString)]

    countries = Country.query.filter_by().all()
    for country in countries:
        searchString = country.search_text 
        inString, inStringList = oneInString(terms, searchString)
        if inString:
            links += [country.url]
            titles += [country.name]
            contexts += [findContexts(inStringList, searchString)]
    
    return (links, titles, contexts)

if __name__ == "__main__" :
    print(searchTermAnd("yuan taiwan"))
    print(searchTermOr("yuan taiwan"))
