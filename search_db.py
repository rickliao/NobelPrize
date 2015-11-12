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
    # find bound (inclusive, exclusive)
    min = len(searchString)
    max = -1
    for query in terms:
        i = searchString.lower().index(query.lower())
        if i < min:
            min = i
        if i+len(query) > max:
            max = i+len(query)
    
    context = searchString[min:max]
    words = re.compile("([^ ]*)( ?)([^ ]*)"+re.escape(context)+"([^ ]*)( ?)([^ ]*)", re.IGNORECASE)
    match = words.search(searchString)
    complete = "..."+match.group(0)+"..."
    for query in terms:
        noCaseQuery = re.compile(re.escape(query), re.IGNORECASE)
        complete = noCaseQuery.sub("~"+query+"~", complete)

    # split phrases to highlight later
    listOfWords = []
    beg = complete.index("~")
    while 1:
        listOfWords += [complete[0:beg]]
        end = complete.index("~", beg+1)
        listOfWords += [complete[beg+1:end]]
        complete = complete[end+1:]
        try:
            beg = complete.index("~")
        except ValueError:
            listOfWords += [complete]
            break
    return listOfWords

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
