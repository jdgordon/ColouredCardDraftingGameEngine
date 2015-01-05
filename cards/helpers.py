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

import random
from collections import deque

from common import *
from . import Cards

def build_card(colour, name, age, cost, players, infostr):
	cardclasses = {
		CARDS_BROWN: Cards.BrownCard,
		CARDS_GREY: Cards.GreyCard,
		CARDS_BLUE: Cards.BlueCard,
		CARDS_GREEN: Cards.GreenCard,
		CARDS_RED: Cards.RedCard,
		CARDS_YELLOW: Cards.YellowCard,
		CARDS_PURPLE: Cards.YellowCard
	}
		
	if not colour in cardclasses:
		return None
	
	card = cardclasses[colour](name, age, cost, players)

	if card != None and card.parse_infotext(infostr):
		if colour == CARDS_PURPLE:
			card.colour = CARDS_PURPLE
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
	for i in range(3):
		total += counts[i] * counts[i]
	return 7 * counts[2] + total

def find_best_score(compass, gear, tablets, choice):
	if len(choice) == 0:
		score = calc_science_score(compass, gear, tablets)
		#print "%d %d %d -> %d" % (compass, gear, tablets, score)
		return ((compass, gear, tablets), score)
	scores = []
	if SCIENCE_COMPASS in choice[0]:
		scores.append(find_best_score(compass + 1, gear, tablets, choice[1:]))
	if SCIENCE_GEAR in choice[0]:
		scores.append(find_best_score(compass, gear + 1, tablets, choice[1:]))
	if SCIENCE_TABLET in choice[0]:
		scores.append(find_best_score(compass, gear, tablets + 1, choice[1:]))
	return sorted(scores, key=lambda score: score[1], reverse=True)[0]

def score_science(player):
	count = {}
	count[SCIENCE_COMPASS] = 0
	count[SCIENCE_GEAR] = 0
	count[SCIENCE_TABLET] = 0
	choice_cards = [] # An array tuples of available choices
	for c in player.get_cards():
		if c.get_colour() == CARDS_GREEN:
			count[c.get_info()] += 1
		elif c.is_science_card():
			choice_cards.append((c.provisions))

	return find_best_score(count[SCIENCE_COMPASS], count[SCIENCE_GEAR], count[SCIENCE_TABLET], choice_cards)
	
def score_military(player, opponent, age):
	my_strength = 0
	their_strength = 0
	points = 0
	
	for c in [c for c in player.get_cards() if c.get_colour() == CARDS_RED]:
		my_strength += c.get_strength()
	for c in [c for c in opponent.get_cards() if c.get_colour() == CARDS_RED]:
		their_strength += c.get_strength()
	
	if my_strength > their_strength:
		points = [1,3,5][age]
	elif my_strength < their_strength:
		points = -1
	#print "WAR: %s: %d %s %d -> %d\b" % (player.name, my_strength, opponent.name, their_strength, points)
	return points

def score_blue(player):
	score = 0
	for c in [c for c in player.get_cards() if c.get_colour() == CARDS_BLUE]:
		score += c.score()
	return score

def score_yellow(player, west_player, east_player):
	score = 0
	for c in [c for c in player.get_cards() if c.get_colour() == CARDS_YELLOW]:
		score += c.score(player, west_player, east_player)
	return score

def score_purple(player, west_player, east_player):
	score = 0
	for c in [c for c in player.get_cards() if c.get_colour() == CARDS_PURPLE]:
		score += c.score(player, west_player, east_player)
	return score
