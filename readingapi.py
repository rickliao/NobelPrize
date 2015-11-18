import urllib.request, json, operator


file = open("albums.json" ,"r")
# url = "http://downing.club/api/releases/"
# response = urllib.request.urlopen(url)
# data = response.read()
jsf = json.loads(file.read())

class Album:
	def __init__(self, name, id, songs, url):
		self.name = name
		self.id = id
		self.songs = songs
		self.url = url

length = []
albuminfo = []
for n in range(0, len(jsf)):
	for x in jsf[0]:
		if(x == "songs"):
			albuminfo.append(Album(jsf[n]["name"], jsf[n]["id"], len(jsf[n][x]), jsf[n]["spotify_url"]))
			length.append(len(jsf[n][x]))

#sort the array and reverse for desired output
albuminfo.sort(key=operator.attrgetter('songs'))
albuminfo.reverse()


for x in albuminfo:
	print("Songs: ",x.songs, ", Album Name: ", x.name, ", ID:", x.id, ", Spotify Url: ",x.url)