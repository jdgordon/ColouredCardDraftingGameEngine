#!/usr/bin/python
import random
from collections import deque

RESOURCE_MONEY 	= "$"
RESOURCE_WOOD 	= "W"
RESOURCE_ORE 	= "O"
RESOURCE_STONE 	= "S"
RESOURCE_BRICK 	= "B"
RESOURCE_GLASS 	= "G"
RESOURCE_LOOM 	= "L"
RESOURCE_PAPER 	= "P"

SCIENCE_GEAR 	= "G"
SCIENCE_COMPASS = "C"
SCIENCE_TABLET 	= "T"

def sort_cards(cards, reverse=False):
	return sorted(cards, key=lambda x: x.get_name(), reverse=reverse)

class Player:
	def __init__(self, name):
		self.name = name
		self.money = 8
		self.tableau = [] # all the players played cards
		self.military = [] # war wins/losses
		self.east_trade_prices = {
			RESOURCE_WOOD: 2,
			RESOURCE_ORE: 2,
			RESOURCE_STONE: 2,
			RESOURCE_BRICK: 2,
			RESOURCE_GLASS: 2,
			RESOURCE_LOOM: 2,
			RESOURCE_PAPER: 2
		}
		self.west_trade_prices = self.east_trade_prices
	
	def is_card_in_tableau(self, card):
		return find_card(self.tableau, card) != None

	def can_build_with_chain(self, card):
		for precard in card.prechains:
			if find_card(self.tableau, precard):
				return True
		return False
		
	def buy_card(self, card, east_player, west_player):
		missing = []
		money_spent = 0
		trade_east = 0
		trade_west = 0
		options = []
		for i in range(len(card.cost)):
			cost = deque(card.cost)
			cost.rotate(i)
			x = self._find_resource_cards(list(cost), east_player, west_player, True)
			if x and x not in options:
					options.append(x)
			x = self._find_resource_cards(list(cost), east_player, west_player, False)
			if x and x not in options:
					options.append(x)
		# we now remove any of the optoins which we cant afford to pay for trades
		for o in options:
			cost = o.coins
			for c in o.east_trades:
				cost += self.east_trade_prices[c.get_info()[0]]
			for c in o.east_trades:
				cost += self.west_trade_prices[c.get_info()[0]]
			if cost > self.money:
				print cost
				options.remove(o)
		return options

	def _find_resource_cards(self, needed_resources, east_cards, west_cards, east_first=True):
		def __check_tableau(r, tableau, used_cards):
			for c in tableau: # FIXME: WONDER too
				if c not in used_cards and (c.get_colour() == "BROWN" or c.get_colour() == "GREY"):
					count = c.provides_resource(r)
					if count == 0:
						continue
					return (c, count)
			return (None, 0)

		used_cards = []
		coins = 0
		east_trades = []
		west_trades = []
		card_sets = [(self.tableau, used_cards)]
		if east_first:
			card_sets += [(east_cards, east_trades), (west_cards, west_trades)]
		else:
			card_sets += [(west_cards, west_trades), (east_cards, east_trades)]
		
		while len(needed_resources):
			r = needed_resources[0]
			found = False
			if r == RESOURCE_MONEY:
				coins += 1
				needed_resources.remove(r)
				continue
			for cards, used in card_sets:
				card, count = __check_tableau(r, cards, used)
				if card and count > 0:
					found = True
					used.append(card)
					for i in range(0, count):
						if r not in needed_resources:
							break
						needed_resources.remove(r)
					break
			if not found:
				return None
		return CardPurchaseOption(used_cards, coins, east_trades, west_trades)
							
			
class CardPurchaseOption:
	def __init__(self, cards, coins, east_trades, west_trades):
		self.cards = cards
		self.coins = coins
		self.east_trades = east_trades
		self.west_trades = west_trades

	def __eq__(self, other):
		return sort_cards(self.cards) == sort_cards(other.cards) and \
			self.coins == other.coins and	\
			sort_cards(self.east_trades) == sort_cards(other.east_trades) and	\
			sort_cards(self.west_trades) == sort_cards(other.west_trades)

	def __repr__(self):
		return "{\n\t%s\n\t$%d\n\tEAST:%s\n\tWEST:%s\n}" % (self.cards, self.coins, self.east_trades, self.west_trades)

class Card:
	def __init__(self, name, age, cost, players):
		self.name = name
		self.age = age
		self.players = players
		self.prechains = []
		self.postchains = []
		valid_resources = [
			RESOURCE_MONEY, RESOURCE_WOOD, RESOURCE_ORE, 
			RESOURCE_STONE, RESOURCE_BRICK, RESOURCE_GLASS, 
			RESOURCE_LOOM, RESOURCE_PAPER]
		card_cost = {}
		self.cost = []
		# This next magic sorts the card cost into an array of required
		# resources from most to least, i.e ['S', 'S', 'S', 'O']
		for r in cost:
			if r in valid_resources:
				if r in card_cost:
					card_cost[r] += 1
				else:
					card_cost[r] = 1
		for x in sorted(card_cost.items(),  key=lambda x: x[1], reverse=True):
			for i in range(0, x[1]):
				self.cost.append(x[0])

	def parse_chains(self, pre, post):
		for card in pre.split("|"):
			self.prechains.append(card.strip())
		for card in post.split("|"):
			self.postchains.append(card.strip())
	
	def parse_infotext(self, text):
		return True
	
	def play(self):
		''' Called when the card is played onto the table'''
		pass
	
	def get_colour(self):
		return ""
		
	def get_info(self):
		return ""

	def __repr__(self):
		return "[%s] %d+ %s (%s) -> %s" % (self.age, self.players, self.name, self.get_colour(), self.get_info())
		
	def get_name(self):
		return self.name

class BrownCard(Card):
	valid_resources = [RESOURCE_WOOD, RESOURCE_ORE, RESOURCE_STONE, RESOURCE_BRICK]
	def parse_infotext(self, text):
		self.resources = {}
		self.allow_all = True
		for r in text:
			if r == "/":
				self.allow_all = False
			elif r in self.valid_resources:
				if r in self.resources:
					self.resources[r] += 1
				else:
					self.resources[r] = 1
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
	
	def provides_resource(self, resource):
		if resource in self.resources:
			return self.resources[resource]
		else:
			return 0

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


def build_card(colour, name, age, cost, players, infostr):
	cardclasses = {
		"brown": BrownCard,
		"grey": GreyCard,
		"blue": BlueCard,
		"green": GreenCard,
		"red": RedCard,
		"yellow": YellowCard,
		"purple": PurpleCard
	}
		
	if not colour in cardclasses:
		return None
	
	card = cardclasses[colour](name, age, cost, players)

	if card != None and card.parse_infotext(infostr):
		return card
	
	print "Error loading card:", name
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
			c = build_card(colour, name, age, cost, players, text)
			if c:
				c.parse_chains(prebuilt, postbuilt)
				cards.append(c)
	print "Loaded %d cards" % ( len(cards))
	return cards

def calc_science_score(compass, gear, tablets):
	counts = sorted([compass, gear, tablets], reverse=True)
	total = 0
	for i in range(0, 2):
		total += counts[i] * counts[i]
	return 7 * counts[2] + total

def find_best_score(compass, gear, tablets, choice):
	if choice == 0:
		score = calc_science_score(compass, gear, tablets)
		#print "%d %d %d -> %d" % (compass, gear, tablets, score)
		return ((compass, gear, tablets), score)
	scr_compass = find_best_score(compass + 1, gear, tablets, choice - 1)
	scr_gear = find_best_score(compass, gear + 1, tablets, choice - 1)
	scr_tablet = find_best_score(compass, gear, tablets + 1, choice - 1)
	return sorted([scr_compass, scr_gear, scr_tablet], key=lambda score: score[1], reverse=True)[0]

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

def find_card(cards, name):
	for c in cards:
		if c.get_name() == name:
			return c
	return None



cards = read_cards_file("7wonders.txt")

PLAYERS = 3
age_1 = [c for c in cards if c.age == 1 and c.players <= PLAYERS]
age_2 = [c for c in cards if c.age == 2 and c.players <= PLAYERS]
age_3 = [c for c in cards if c.age == 3 and c.get_colour() != "PURPLE" and c.players <= PLAYERS]
purple = [c for c in cards if c.age == 3 and c.get_colour() == "PURPLE" and c.players <= PLAYERS]


random.shuffle(age_1)
random.shuffle(age_2)
random.shuffle(purple)
age_3 += purple[0 : PLAYERS + 2]
random.shuffle(age_3)


p1 = age_1[0:7] + age_2[0:7] + age_3[0:7]
p2 = age_1[7:14] + age_2[7:14] + age_3[7:14]
p3 = age_1[14:21] + age_2[14:21] + age_3[14:21]

players = []
for i in range(0, PLAYERS):
	players.append(Player("player %d" % (i + 1)))

p = players[0]
p.tableau += [cards[1], cards[3], find_card(cards, "glassworks")]
print p.tableau

#print p._find_resource_cards(['W', 'S', 'W'])

print p.buy_card(find_card(cards, "dispensary"), [find_card(cards, "forest cave")], [find_card(cards, "forest cave")])


