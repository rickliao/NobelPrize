import urllib.request, json, operator


file = open("albums.json" ,"r")
afile = open("artists.json", "r")
# url = "http://downing.club/api/releases/"
# response = urllib.request.urlopen(url)
# data = response.read()
jsf = json.loads(file.read())
ajsf = json.loads(afile.read())

class Album:
	def __init__(self, name, id, songs, url, artist):
		self.name = name
		self.id = id
		self.songs = songs
		self.url = url
		self.artist = artist

	def setArtist(self, a):
		self.artist = a

class Artist:
	def __init__(self, name, id, url):
		self.name = name
		self.id = id
		self.url = url
		self.songs = 0

	def addSongs(self, a):
		self.songs += a

length = []
albuminfo = []
artistinfo = []
for n in range(0, len(jsf)):
	for x in jsf[0]:
		if(x == "songs"):
			albuminfo.append(Album(jsf[n]["name"], jsf[n]["id"], len(jsf[n][x]), jsf[n]["spotify_url"], jsf[n]["artists"][0]["uri"]))
			length.append(len(jsf[n][x]))

#sort the array and reverse for desired output
albuminfo.sort(key=operator.attrgetter('songs'))
albuminfo.reverse()

for n in range(0, len(ajsf)):
	artistinfo.append(Artist(ajsf[n]["name"], ajsf[n]["id"], ajsf[n]["uri"]))

for x in albuminfo:
	for n in artistinfo:
		if x.artist == n.url:
			n.addSongs(x.songs)
			#print("Songs: ",x.songs, ", Artist Name: ", n.name, ", Album Name: ", x.name, ", ID:", x.id, ", Spotify Url: ",x.url)


artistinfo.sort(key=operator.attrgetter('songs'))
artistinfo.reverse()
for n in artistinfo:
	print(n.songs,  n.name)
