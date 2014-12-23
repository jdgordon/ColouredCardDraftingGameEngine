#!/usr/bin/python
import random

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
	def __init__(self, name, age, players):
		self.name = name
		self.age = age
		self.players = players
	
	def parse_infotext(self, text):
		return True
	
	def play(self):
		''' Called when the card is played onto the table'''
		pass
	
	def get_colour(self):
		return ""
		
	def get_info(self):
		return ""

	def get_name(self):
		return "[%s] %d+ %s (%s) -> %s" % (self.age, self.players, self.name, self.get_colour(), self.get_info())
		
	def __repr__(self):
		return self.get_name()

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

class RedCard(Card):
	def parse_infotext(self, text):
		self.strength = int(text)
		return True
	
	def get_info(self):
		return "%d" % (self.strength)

	def get_colour(self):
		return "RED"
	
	def get_strength(self):
		return self.strength

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
	
	def gives_science(self):
		return False


def build_card(colour, name, age, players, infostr):
	card = None
	if colour == "brown":
		card = BrownCard(name, age, players)
	elif colour == "grey":
		card = GreyCard(name, age, players)
	elif colour == "blue":
		card = BlueCard(name, age, players)
	elif colour == "green":
		card = GreenCard(name, age, players)
	elif colour == "red":
		card = RedCard(name, age, players)
	elif colour == "yellow":
		card = YellowCard(name, age, players)
	elif colour == "purple":
		card = PurpleCard(name, age, players)

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
			c = build_card(colour, name, age, players, text)
			if c:
				cards.append(c)
	return cards

def calc_science_score(compass, gear, tablets):
	counts = sorted([compass, gear, tablets], reverse=True)
	total = 0
	for i in range(0, 2):
		total += counts[i] * counts[i]
	return 7 * counts[2] + total

def find_best_score(compass, gear, tablets, choice):
	if choice == 0:
		#print "%d %d %d -> %d" % (compass, gear, tablets, calc_science_score(compass, gear, tablets))
		return calc_science_score(compass, gear, tablets)
	scr_compass = find_best_score(compass + 1, gear, tablets, choice - 1)
	scr_gear = find_best_score(compass, gear + 1, tablets, choice - 1)
	scr_tablet = find_best_score(compass, gear, tablets + 1, choice - 1)
	return sorted([scr_compass, scr_gear, scr_tablet], reverse=True)[0]

def score_science(player_cards):
	count = {}
	count[SCIENCE_COMPASS] = 0
	count[SCIENCE_GEAR] = 0
	count[SCIENCE_TABLET] = 0
	choice_cards = 0
	for c in player_cards:
		if c.get_colour() == "GREEN":
			count[c.get_info()] += 1
		elif c.get_colour() == "PURPLE" and c.gives_science():
			choice_cards += 1

	return find_best_score(count[SCIENCE_COMPASS], count[SCIENCE_GEAR], count[SCIENCE_TABLET], choice_cards)
	
def score_military(player, opponent, age):
	my_strength = 0
	their_strength = 0
	
	for c in [c for c in player if c.get_colour() == "RED"]:
		my_strength += c.get_strength()
	for c in [c for c in opponent if c.get_colour() == "RED"]:
		their_strength += c.get_strength()
	
	if my_strength > their_strength:
		return [1,3,5][age - 1]
	elif my_strength < their_strength:
		return -1
	else:
		return 0

def score_blue(player):
	score = 0
	for c in [c for c in player if c.get_colour() == "BLUE"]:
		score += c.score()
	return score

cards = read_cards_file("7wonders.txt")

age_1 = [c for c in cards if c.age == 1]
age_2 = [c for c in cards if c.age == 2]
age_3 = [c for c in cards if c.age == 3 and c.get_colour() != "PURPLE"]
purple = [c for c in cards if c.age == 3 and c.get_colour() == "PURPLE"]


random.shuffle(age_1)
random.shuffle(age_2)
age_3 += purple[0:5]
random.shuffle(age_3)

PLAYERS = 3
p1 = age_1[0:7] + age_2[0:7] + age_3[0:7]
p2 = age_1[7:14] + age_2[7:14] + age_3[7:14]
p3 = age_1[14:21] + age_2[14:21] + age_3[14:21]

print score_science(p1)
print score_military(p1, p2, 3)
print score_blue(p1)



