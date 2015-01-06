#!/usr/bin/python
#
# Copyright 2015 - Jonathan Gordon
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This software is distributed on an "AS IS" basis, WITHOUT WARRANTY OF ANY
# KIND, either express or implied.

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
			for i in range(x[1]):
				self.cost.append(x[0])

	def parse_chains(self, pre, post):
		for card in pre.split("|"):
			self.prechains.append(card.strip())
		for card in post.split("|"):
			self.postchains.append(card.strip())

	def parse_infotext(self, text):
		return True

	def play(self, player, west_player, east_player):
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

	def get_cost(self):
		return self.cost

	def get_cost_as_string(self):
		out = ""
		for r in self.get_cost():
			out += r
		return out

	def is_resource_card(self): #generally brown/grey and some yellow
		return (False, False) # (resource card, tradeable)
	def is_science_card(self): # generally green
		return False
	def is_war_card(self): # generally red
		return False
	def is_guild_card(self): # purple
		return False

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

	def pretty_print_name(self, with_info=True):
		if with_info:
			info = " %s" % (self.get_info())
		else:
			info = ""
		return "%s%s%s%s" % (self.get_ascii_colour(), self.get_name(), info, '\033[0m')

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
			text += r * self.resources[r]
		return text

	def provides_resource(self, resource):
		if resource in self.resources:
			return self.resources[resource]
		else:
			return 0

	def get_colour(self):
		return CARDS_BROWN

	def is_resource_card(self):
		return (True, True)

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

	def is_science_card(self):
		return True

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

	def is_war_card(self):
		return True

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
		while len(text) and text[0] == RESOURCE_MONEY:
			money += 1
			text = text[1:]
		return (money, text)
	def _get_points_count(self, text):
		points = 0
		while len(text) and text[0] == RESOURCE_VICTORYPOINT:
			points += 1
			text = text[1:]
		return (points, text)
	def _get_squigly_text(self, text, splitter="|"):
		''' returns the array of items inside the {}'s and the text immediatly after'''
		out = []
		if not "{" in text:
			return ([], text)
		start = text.index("{")
		end = text.index("}")
		items = text[start + 1:end].split(splitter)
		for i in range(len(items)):
			items[i] = items[i].strip()
		return (items, text[end + 1:])

	def _count_cards(self, colour, player):
		count = 0
		# check special cases
		if colour == "war lose":
			for warscore in player.military:
				if warscore < 0:
					count += 1
		elif colour == "war win":
			for warscore in player.military:
				if warscore > 0:
					count += 1
		#elif colour == "wonder":
		#	count = player.wonder.built_stages
		else:
			for c in player.get_cards():
				if c.get_colour() == colour:
					count += 1
		return count

	def get_info(self):
		return self.text

	def get_colour(self):
		return "-----"

class TradeCardInfo():
	def __init__(self, value, resources, directions):
		self.value = value
		self.resources = resources
		self.directions = directions

class GainCardInfo():
	def __init__(self, moneygain, pointsgain, colours, directions):
		self.money = moneygain
		self.points = pointsgain
		self.colours = colours
		self.directions = directions

class YellowCard(FooPlaceHolderCard):
	def parse_infotext(self, text):
		self.colour = CARDS_YELLOW
		# init the different things this card could be
		self.trade_card_info = None
		self.gain_card_info = None
		self.provides_resources = False
		self.provides_science = False

		self.text = text

		if text.startswith(INFOPREFIX_TRADE):
			return self.parse_trade_card(text[len(INFOPREFIX_TRADE):])
		elif text.startswith(INFOPREFIX_PROVIDER):
			return self.parse_provider_card(text[len(INFOPREFIX_PROVIDER):])
		else:
			return self.parse_gain_card(text)
		return True

	def get_colour(self):
		return self.colour

	def play(self, player, east_player, west_player):
		if self.trade_card_info:
			if DIRECTION_EAST in self.trade_card_info.directions:
				for r in self.trade_card_info.resources:
					player.east_trade_prices[r] += self.trade_card_info.value
			if DIRECTION_WEST in self.trade_card_info.directions:
				for r in self.trade_card_info.resources:
					player.west_trade_prices[r] += self.trade_card_info.value
			#print "TRADE: ", player.east_trade_prices, player.west_trade_prices
		elif self.gain_card_info:
			count = 0
			for c in self.gain_card_info.colours:
				if DIRECTION_WEST in self.gain_card_info.directions:
					count += self._count_cards(c, west_player)
				if DIRECTION_SELF in self.gain_card_info.directions:
					count += self._count_cards(c, player)
				if DIRECTION_EAST in self.gain_card_info.directions:
					count += self._count_cards(c, east_player)
			player.money += count * self.gain_card_info.money

	def score(self, player, west_player, east_player):
		if self.gain_card_info:
			count = 0
			for c in self.gain_card_info.colours:
				if DIRECTION_WEST in self.gain_card_info.directions:
					count += self._count_cards(c, west_player)
				if DIRECTION_SELF in self.gain_card_info.directions:
					count += self._count_cards(c, player)
				if DIRECTION_EAST in self.gain_card_info.directions:
					count += self._count_cards(c, east_player)
			return count * self.gain_card_info.points
		return 0

	def parse_trade_card(self, text):
		decrement = text[0] == "-"
		money, text = self._get_money_count(text[1:])
		resources = []
		while text[0] != "}":
			if text[0] in ALL_RESOURCES:
				resources.append(text[0])
			text = text[1:]
		directions = self._get_card_directions(text)
		if decrement:
			money *= -1
		self.trade_card_info = TradeCardInfo(money, resources, directions)
		return True

	def parse_provider_card(self, text):
		if text.startswith("resource"):
			self.provides_resources = True
		elif text.startswith("science"):
			self.provides_science = True

		self.provisions, text = self._get_squigly_text(text, splitter="/")
		return True

	def is_resource_card(self):
		return (self.provides_resource, False)

	def provides_resource(self, resource):
		if self.provides_resources and resource in self.provisions:
			return 1
		return 0

	def is_science_card(self):
		return self.provides_science

	def parse_gain_card(self, text):
		money, text = self._get_money_count(text)
		points, text = self._get_points_count(text)
		colours, text = self._get_squigly_text(text)
		directions = self._get_card_directions(text)
		if len(directions) == 0:
			directions.append(DIRECTION_SELF)
		self.gain_card_info = GainCardInfo(money, points, colours, directions)
		return True

class PurpleCard(FooPlaceHolderCard):
	def get_colour(self):
		return CARDS_PURPLE

	def gives_science(self):
		return False

	def is_guild_card(self):
		return True

