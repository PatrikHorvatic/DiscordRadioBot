import os

class Podaci:
	def __init__(self):
		self.TOKEN = os.getenv("TOKEN")
		self.PREFIX = os.getenv("PREFIX")
		self.STANICE = {
			"RADIO101": "http://live.radio101.hr:9531/",
            "RADIO101-ROCK": "http://live.radio101.hr:9578/",

			"HRT-HR1":
			"https://playerservices.streamtheworld.com/api/livestream-redirect/PROGRAM1.mp3",
			"HRT-HR2":
			"https://playerservices.streamtheworld.com/api/livestream-redirect/PROGRAM2.mp3",
			"HRT-HR3": "https://playerservices.streamtheworld.com/api/livestream-redirect/PROGRAM3.mp3",

			"MEGATON": "https://chopin.bizmusic.net/radio/8030/radio.mp3",
			"LUDBREG": "http://85.25.135.86:23573/;*.nsv",
			"SJEVERNI-FM": "https://live.sjeverni.fm/radio/8000/radio.mp3",
			"EXTRA-FM": "http://streams.extrafm.hr:8110/",
			"LAGANINI-FM": "http://194.145.208.251:8000/start/lfmzg",
            
			"MAX": "https://chopin.bizmusic.net/radio/8030/",
			"KAJ": "https://stream.rcast.net/66509",
			"BANOVINA": "http://stream1.radio-banovina.hr:9998/stream",
			"VESELJAK-IVANEC": "http://sirius.shoutca.st:10204/stream",
			"MAESTRAL": "http://178.218.163.171:8003/;stream.mp3",

			"OTVORENI": "https://stream.otvoreni.hr:443/otvoreni",
			"OTVORENI-LOVE": "https://stream.otvoreni.hr:443/love",
			"OTVORENI-FITNESS": "https://stream.otvoreni.hr:443/fitness",
			"OTVORENI-CHILL": "https://stream.otvoreni.hr:443/chill",
			"OTVORENI-HOT": "https://stream.otvoreni.hr:443/hot",

			"ANTENA": "http://live.antenazagreb.hr:8000/",
			"ANTENA-ROCK": "http://live.antenazagreb.hr:8019/",
			"ANTENA-MIX": "http://live.antenazagreb.hr:8015/",
			"ANTENA-HIT": "http://live.antenazagreb.hr:8011/",
			"ANTENA-LOVE": "http://live.antenazagreb.hr:8007/",

			"GOLD-FM": "http://live.goldfm.hr:8068/;stream.nsv",
			"GOLD-ROCK": "http://live.goldfm.hr:8169/;",
			"GOLD-PARTY": "http://live.goldfm.hr:8136/;",
			"GOLD-OLDIES": "http://live.goldfm.hr:8118/;",
			"GOLD-XMAS": "http://live.goldfm.hr:8269/;stream.nsv",
			"GOLD-EXYU": "http://c5.hostingcentar.com:8157/;stream.nsv",

			"NARODNI-VESELO": "http://live.narodni.hr:8051/",
			"NARODNI": "http://live.narodni.hr:8059/",
			"NARODNI-LJUBAV": "http://live.narodni.hr:8181/",
			"NARODNI-SAMOSVIRAJ": "http://live.narodni.hr:8175/",
			"NARODNI-AAAAAAA": "http://live.narodni.hr:8045/",
			"NARODNI-OPUŠTENO": "http://live.narodni.hr:8039/"
            }
		self.player = None
		self.radioStanica = None
		self.aktivnaStanica = None