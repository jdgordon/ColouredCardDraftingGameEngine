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

