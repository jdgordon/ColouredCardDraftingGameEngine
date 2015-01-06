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
import cards

class Logger:
	def __init__(self):
		self.log = []
		self.card_list = []
	
	def _get_age_string(self):
		return ["I", "II", "III"][self.current_age]
	
	def log_age_header(self, age):
		self.current_age = age
		self.log.append("Starting age %s" % (self._get_age_string()))

	def log_action(self, player, action, card):
		text = "%s " % (player.get_name())
		if action == ACTION_PLAYCARD:
			text += "player %s, using blaa...." % (card.pretty_print_name())
		elif action == ACTION_DISCARD:
			text += "discarded an age %s card for $3" % (self._get_age_string())
		elif action == ACTION_STAGEWONDER:
			text += "discarded an age %s card fto build the next wonder stage" % (self._get_age_string())
		
		self.log.append(text)
	
	def log_buy_card_with_chain(self, player, card):
		text = "%s " % (player.get_name())
		text += "played %s (for free with %s)" % (card.pretty_print_name(), find_card(self.card_list, card.prechains[0]).pretty_print_name())
		self.log.append(text)
	
	def log_buy_card(self, player, card, how):
		text = "%s " % (player.get_name())
		text += "played %s " % (card.pretty_print_name())
		if how.coins or how.east_cost or how.west_cost:
			text += "paying "
			if how.coins:
				text += "$%d to the bank, " % ( how.coins)
			if how.west_cost:
				text += "$%d to the player to his left, " % ( how.west_cost)
			if how.east_cost:
				text += "$%d to the player to his right, " % ( how.east_cost)
			text = text[0:-2] + "."
		self.log.append(text)
	
	def log_military_battle(self, player, player_strength, opponent, opponent_strength, score):
		if player_strength > opponent_strength:
			text = "%s with %d shields defeated %s with %d shields taking %d points." % (player, player_strength, opponent, opponent_strength, score)
		elif player_strength < opponent_strength:
			text = "%s with %d shields was defeated by %s with %d shields losing %d points." % (player, player_strength, opponent, opponent_strength, score)
		else:
			text = "%s and %s both have %d strength, No points awarded." % ( player, opponent, player_strength)
		self.log.append(text)
	
	def log_freetext(self, text):
		self.log.append(text)
	
	def dump(self, file):
		for line in self.log:
			file.write(line + "\n")

