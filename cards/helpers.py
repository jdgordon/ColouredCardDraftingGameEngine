#!/usr/bin/python
import random
from collections import deque

from common import *
from . import Cards

def build_card(colour, name, age, cost, players, infostr):
	cardclasses = {
		"brown": Cards.BrownCard,
		"grey": Cards.GreyCard,
		"blue": Cards.BlueCard,
		"green": Cards.GreenCard,
		"red": Cards.RedCard,
		"yellow": Cards.YellowCard,
		"purple": Cards.PurpleCard
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
