import requests

class Dadjoke:

    def __init__(self):
        self.url = "https://dad-jokes.p.rapidapi.com/random/joke"
        self.headers = {
    'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
    'x-rapidapi-key': "dc70f6fd4dmshcd92df3a5ab867dp122ee0jsn4c75877a366f"
    }
        
    def dohvatiForu(self):
        self.fora = ""
        self.response = requests.request("GET", self.url, headers=self.headers)
        self.odgovor = self.response.json()
        fora = f"""{self.odgovor["body"][0]["setup"]} {self.odgovor["body"][0]["punchline"]}"""
        return fora