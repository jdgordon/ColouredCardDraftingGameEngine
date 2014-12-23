#!/usr/bin/python

RESOURCE_WOOD = "W"
RESOURCE_ORE = "O"
RESOURCE_STONE = "S"
RESOURCE_BRICK = "B"
RESOURCE_GLASS = "G"
RESOURCE_LOOM = "L"
RESOURCE_PAPER = "P"

SCIENCE_GEAR = "G"
SCIENCE_COMPASS = "C"
SCIENCE_TABLET = "T"

class Card:
	def __init__(self, name):
		self.name = name
		self.age = "1"
	
	def parse_infotext(self, text):
		return True
	
	def play(self):
		''' Called when the card is played onto the table'''
		pass
	
	def score(self):
		''' Called when the card needs to score itself end game'''
		pass
	
	def get_colour(self):
		return ""
		
	def get_info(self):
		return ""

	def get_name(self):
		return self.name + " (" + self.get_colour() + ")" + " -> " + self.get_info()

class BrownCard(Card):
	valid_resources = [RESOURCE_WOOD, RESOURCE_ORE, RESOURCE_STONE, RESOURCE_BRICK]
	def parse_infotext(self, text):
		self.resources = []
		self.allow_all = True
		for r in text:
			if r == "/":
				self.allow_all = False
			elif r in self.valid_resources:
				self.resources.append(r)
			else:
				return False
		return True
	
	def get_info(self):
		text = ""
		for r in self.resources:
			if len(text) != 0:
				if self.allow_all == False:
					text += "/"
			text += r
		return text

	def get_colour(self):
		return "BROWN"
		
class GreyCard(BrownCard):
	valid_resources = [RESOURCE_GLASS, RESOURCE_LOOM, RESOURCE_PAPER]
	def get_colour(self):
		return "GREY"
	
class BlueCard(Card):
	def parse_infotext(self, text):
		self.points = int(text)
		return True

	def get_colour(self):
		return "BLUE"
		
	def get_info(self):
		return "%d points" %(self.points)

	def score(self):
		return self.points

class GreenCard(Card):
	def parse_infotext(self, text):
		if text[0] in [SCIENCE_COMPASS, SCIENCE_GEAR, SCIENCE_TABLET]:
			self.group = text[0]
			return True
		return False
	
	def get_info(self):
		return self.group

	def get_colour(self):
		return "GREEN"

class FooPlaceHolderCard(Card):
	def parse_infotext(self, text):
		self.text = text
		return True
	
	def get_info(self):
		return self.text

	def get_colour(self):
		return "-----"
		
class YellowCard(FooPlaceHolderCard):
	def get_colour(self):
		return "YELLOW"

class PurpleCard(FooPlaceHolderCard):
	def get_colour(self):
		return "PURPLE"


def build_card(colour, name, infostr):
	card = None
	if colour == "brown":
		card = BrownCard(name)
	elif colour == "grey":
		card = GreyCard(name)
	elif colour == "blue":
		card = BlueCard(name)
	elif colour == "green":
		card = GreenCard(name)
	elif colour == "yellow":
		card = YellowCard(name)
	elif colour == "purple":
		card = PurpleCard(name)
	
	if card != None and card.parse_infotext(infostr):
		return card
	
	return None


def read_cards_file(filename):
	cards = []
	with open(filename) as f:
		content = f.readlines()
		for line in content:
			if line.startswith("#"):
				continue
			values = line.split(",")
			if len(values) != 8:
				continue
			age = int(values[0].strip())
			players = int(values[1].strip())
			name = values[2].strip()
			colour = values[3].strip()
			cost = values[4].strip()
			prebuilt = values[5].strip()
			postbuilt = values[6].strip()
			text = values[7].strip()
			c = build_card(colour, name, text)
			if c:
				cards.append(c)
	return cards
			

cards = read_cards_file("7wonders.txt")
for c in cards:
	print c.get_name()
