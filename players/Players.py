
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

from collections import deque
from common import *
import cards

class Player:
	def __init__(self, name):
		self.name = name
		self.money = 3
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
		self.west_trade_prices = self.east_trade_prices.copy()
		self.wonder = None
		self.personality = None
	
	def set_personality(self, persona):
		self.personality = persona
	
	def get_cards(self):
		return self.tableau
	
	def play_hand(self, hand, west_player, east_player):
		''' return the card and action done'''
		options = []
		for card in hand:
			#print card.get_name(), self.is_card_in_tableau(card)
			if not self.is_card_in_tableau(card):
				if self.can_build_with_chain(card):
					options.append((ACTION_PLAYCARD, card))
				elif self.buy_card(card, west_player, east_player):
					options.append((ACTION_PLAYCARD, card))
			options.append((ACTION_DISCARD, card))
			if False:#self.wonder.built_stages < 3: #FIXMEself.wonder.stages:
				options.append((ACTION_STAGEWONDER, card))
		i = 0
		print "-=================-"
		
		options = sorted(options, key=lambda x: {CARDS_GREY:0, CARDS_BROWN:1, CARDS_YELLOW:2, CARDS_BLUE:3, CARDS_RED:4, CARDS_GREEN:5, CARDS_PURPLE:6}[x[1].get_colour()])
		for o in options:
			actions = { ACTION_PLAYCARD:"Play", ACTION_DISCARD:"Discard", ACTION_STAGEWONDER:"Stage" }
			card = o[1]
			print "[%d]: %s\t%s\t%s" % (i, actions[o[0]], card.get_cost_as_string(), card.pretty_print_name())
			i += 1
		print "-=================-"

		return options[self.personality.make_choice(options)]
	
	def print_tableau(self):
		cards = { CARDS_BROWN:[], CARDS_GREY:[], CARDS_YELLOW:[], CARDS_BLUE:[], CARDS_RED:[], CARDS_GREEN:[], CARDS_PURPLE:[] }
		print "You have $%d" % (self.money)
		print "War points: %s" % (self.military)
		print self.west_trade_prices
		print self.east_trade_prices
		for c in self.get_cards():
			cards[c.get_colour()].append(c)
		
		biggest_deck = 0
		for colour in cards.keys():
			count =  len(cards[colour])
			if count > biggest_deck:
				biggest_deck = count
		for i in range(biggest_deck):
			line = { CARDS_BROWN:"\t", CARDS_GREY:"\t", CARDS_YELLOW:"\t", CARDS_BLUE:"\t", CARDS_RED:"\t", CARDS_GREEN:"\t", CARDS_PURPLE:"\t" }
			for colour in [CARDS_BROWN, CARDS_GREY, CARDS_YELLOW, CARDS_BLUE, CARDS_RED, CARDS_GREEN, CARDS_PURPLE]:
				if len(cards[colour]) > biggest_deck - 1 - i:
					line[colour] = "%s" % (cards[colour][biggest_deck - 1 - i].pretty_print_name())
				else:
					line[colour] = "        "
			
			print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % ( line[CARDS_BROWN], line[CARDS_GREY], line[CARDS_YELLOW], line[CARDS_BLUE], line[CARDS_RED], line[CARDS_GREEN],line[CARDS_PURPLE])
		
	
	def set_wonder(self, wonder):
		self.wonder = wonder
	
	def is_card_in_tableau(self, card):
		return find_card(self.get_cards(), card.get_name()) != None

	def can_build_with_chain(self, card):
		for precard in card.prechains:
			if find_card(self.get_cards(), precard):
				return True
		return False
		
	def buy_card(self, card, west_player, east_player):
		missing = []
		money_spent = 0
		trade_east = 0
		trade_west = 0
		options = []
		if len(card.cost) == 0:
			return [CardPurchaseOption([], 0, [], [])]
		for i in range(len(card.cost)):
			cost = deque(card.cost)
			cost.rotate(i)
			for east_first in [True, False]:
				x = self._find_resource_cards(list(cost), west_player.get_cards(), east_player.get_cards(), east_first)
				if x and x not in options:
					options.append(x)
		# we now remove any of the options which we cant afford to pay for trades
		legal_options = []
		for o in options:
			cost = o.coins
			for c in o.east_trades:
				o.east_cost = self.east_trade_prices[c.resource] * c.count
				cost += o.east_cost
			for c in o.west_trades:
				o.west_cost = self.west_trade_prices[c.resource] * c.count
				cost += o.west_cost
			if cost <= self.money:
				o.set_total(cost)
				legal_options.append(o)
			# Setting the total cost is buggy
		#print sorted(legal_options, key=lambda x: x.total_cost)
		return sorted(legal_options, key=lambda x: x.total_cost)

	def _find_resource_cards(self, needed_resources, west_cards, east_cards, east_first=True):
		def __is_card_used(card, used_cards_array):
			for x in used_cards_array:
				if card == x.card:
					return True
			return False
		def __check_tableau(r, tableau, used_cards, tradeable_only):
			for c in tableau: # FIXME: WONDER too
				if not __is_card_used(c, used_cards):
					is_resource, tradeable = c.is_resource_card()
					if is_resource and ((not tradeable_only) or (tradeable_only == tradeable)):
						count = c.provides_resource(r)
						if count == 0:
							continue
						return (c, count)
			return (None, 0)

		used_cards = []
		coins = 0
		east_trades = []
		west_trades = []
		card_sets = [(self.get_cards(), used_cards, False)]
		if east_first:
			card_sets += [(east_cards, east_trades, True), (west_cards, west_trades, True)]
		else:
			card_sets += [(west_cards, west_trades, True), (east_cards, east_trades, True)]
		
		while len(needed_resources):
			r = needed_resources[0]
			found = False
			if r == RESOURCE_MONEY:
				coins += 1
				needed_resources.remove(r)
				continue
			for cards, used, tradeable_only in card_sets:
				card, count = __check_tableau(r, cards, used, tradeable_only)
				if card and count > 0:
					found = True
					needed_count = 0
					for i in range(0, count):
						if r not in needed_resources:
							break
						needed_count += 1
						needed_resources.remove(r)
					used.append(CardPurchaseUse(card, r, needed_count))
					break
			if not found:
				return None
		return CardPurchaseOption(used_cards, coins, west_trades, east_trades)

class CardPurchaseUse:
	def __init__(self, card, resource, count):
		self.card = card
		self.resource = resource
		self.count = count
	
	def __eq__(self, other):
		return self.resource == other.resource \
			and self.count == other.count \
			and self.card.get_name() == other.card.get_name()
	
	def __repr__(self):
		if len(self.card.get_info()) == 1:
			return "%s"% (self.card)
		return "%s -> %s * %d" % (self.card, self.resource, self.count)
			
class CardPurchaseOption:
	def __init__(self, cards, coins, west_trades, east_trades):
		self.cards = cards
		self.coins = coins
		self.west_trades = west_trades
		self.east_trades = east_trades
		self.total_cost = 0
		self.east_cost = 0
		self.west_cost = 0
	
	def set_total(self, cost):
		self.total_cost = cost

	def __eq__(self, other):
		if self.coins != other.coins:
			return False
		for us, them in [(self.cards, other.cards), \
						(self.west_trades, other.west_trades), \
						(self.east_trades, other.east_trades)]:
			if len(us) != len(them):
				return False
			for x in us:
				if x not in them:
					return False
				
		return True

	def __repr__(self):
		return "{ (total: $%d)\n\t%s\n\t$%d\n\tWEST:%s\n\tEAST:%s\n}" % (self.total_cost, self.cards, self.coins, self.west_trades, self.east_trades)
