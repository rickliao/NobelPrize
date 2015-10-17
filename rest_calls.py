import requests
import json

def getPrize() :
    response = requests.get("http://api.nobelprize.org/v1/prize.json?year=2008&category=economics")
    if response.ok :
    	jsonData = json.loads(response.text)
    	print(jsonData)

    response = requests.get("http://api.nobelprize.org/v1/prize.json?year=2015&category=physics")
    if response.ok :
    	jsonData = json.loads(response.text)
    	print(jsonData)

    response = requests.get("http://api.nobelprize.org/v1/prize.json?year=1964&category=chemistry")
    if response.ok :
    	jsonData = json.loads(response.text)
    	print(jsonData)

if __name__ == '__main__':
	getPrize()