import requests

class Deezer():

    rjecnikPoveznica = dict()

    def __init__(self,umjetnik):
        self.url = "https://deezerdevs-deezer.p.rapidapi.com/search"
        self.headers = {
        	'x-rapidapi-key': "dc70f6fd4dmshcd92df3a5ab867dp122ee0jsn4c75877a366f",
    		'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com"
    		}
        self.querystring = {"q":umjetnik}
    
    def DohvatiPodatke(self):
        self.response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
        self.podaci = self.response.json()
		#print(self.podaci)
    
    def SpremiRjecnikPoveznica(self):
        if "error" in self.podaci:
            print("API izbacio grešku. Pokušaj kasnije.")
        else:
            for i in range(1,25):
                self.rjecnikPoveznica[self.podaci["data"][i]["title"]] = [self.podaci["data"][i]["link"]]
            return self.rjecnikPoveznica