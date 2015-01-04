#!/usr/bin/python
from common import *

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
	
	def play(self, player, east_player, west_player):
		''' Called when the card is played onto the table'''
		pass
	
	def get_colour(self):
		return ""
		
	def get_info(self):
		return ""

	def __repr__(self):
		return "%s (%s) -> %s" % (self.name, self.get_colour(), self.get_info())
		
	def get_name(self):
		return self.name
	
	def get_ascii_colour(self):
		return {
			CARDS_BROWN: '\033[33m',
			CARDS_GREY: '\033[37m',
			CARDS_RED: '\033[31m',
			CARDS_GREEN: '\033[92m',
			CARDS_YELLOW: '\033[1;33m',
			CARDS_BLUE: '\033[34m',
			CARDS_PURPLE: '\033[35m',
			}[self.get_colour()]
	
	def pretty_print_name(self):
		return "%s%s%s" % (self.get_ascii_colour(), self.get_name(), '\033[0m')

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
		return CARDS_BROWN
		
class GreyCard(BrownCard):
	valid_resources = [RESOURCE_GLASS, RESOURCE_LOOM, RESOURCE_PAPER]
	def get_colour(self):
		return CARDS_GREY
	
class BlueCard(Card):
	def parse_infotext(self, text):
		self.points = int(text)
		return True

	def get_colour(self):
		return CARDS_BLUE
		
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
		return CARDS_GREEN

class RedCard(Card):
	def parse_infotext(self, text):
		self.strength = int(text)
		return True
	
	def get_info(self):
		return "%d" % (self.strength)

	def get_colour(self):
		return CARDS_RED
	
	def get_strength(self):
		return self.strength

class FooPlaceHolderCard(Card):
	def parse_infotext(self, text):
		self.text = text
		return True
	
	def _get_card_directions(self, text):
		ret = []
		for direction in [DIRECTION_EAST, DIRECTION_SELF, DIRECTION_WEST]:
			if direction in text:
				ret.append(direction)
		return ret
	def _get_money_count(self, text):
		money = 0
		while text[0] == RESOURCE_MONEY:
			money += 1
			text = text[1:]
		return (money, text)
	def _get_squigly_text(self, text):
		''' returns the array of items inside the {}'s and the text immediatly after'''
		out = []
		if not "{" in text:
			return ([], text)
		start = text.index("{")
		end = text.index("}")
		items = text[start + 1:end].split("|")
		for i in range(0, len(items)):
			items[i] = items[i].strip()
		return (items, text[end + 1:])

	def _count_cards(self, colour, player):
		count = 0
		for c in player.tableau:
			if c.get_colour() == colour:
				count += 1
		return count

	def get_info(self):
		return self.text

	def get_colour(self):
		return "-----"
		
class YellowCard(FooPlaceHolderCard):
	def get_colour(self):
		return CARDS_YELLOW
		
	def play(self, player, east_player, west_player):
		if self.text[0] == "-": # affects trade values, probably wont scale
			money, text = self._get_money_count(self.text[1:])
			resources = []
			while text[0] != "}":
				if text[0] in ALL_RESOURCES:
					resources.append(text[0])
				text = text[1:]
			directions = self._get_card_directions(text)
			if DIRECTION_EAST in directions:
				for r in resources:
					player.east_trade_prices[r] -= money
			if DIRECTION_WEST in directions:
				for r in resources:
					player.west_trade_prices[r] -= money
		elif self.text[0] == RESOURCE_MONEY: # money/points for something
			money, text = self._get_money_count(self.text[1:])
			colours, text = self._get_squigly_text(text)
			directions = self._get_card_directions(text)
			count = 0
			for c in colours:
				if DIRECTION_WEST in directions:
					count += self._count_cards(c, west_player)
				if DIRECTION_SELF in directions:
					count += self._count_cards(c, player)
				if DIRECTION_EAST in directions:
					count += self._count_cards(c, east_player)
			player.money += count * money
				
				

class PurpleCard(FooPlaceHolderCard):
	def get_colour(self):
		return CARDS_PURPLE
	
	def gives_science(self):
		return False

