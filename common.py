#!/usr/bin/python

RESOURCE_MONEY 	= "$"
RESOURCE_WOOD 	= "W"
RESOURCE_ORE 	= "O"
RESOURCE_STONE 	= "S"
RESOURCE_BRICK 	= "B"
RESOURCE_GLASS 	= "G"
RESOURCE_LOOM 	= "L"
RESOURCE_PAPER 	= "P"

ALL_RESOURCES = {	\
	RESOURCE_MONEY, RESOURCE_WOOD, RESOURCE_ORE,	\
	RESOURCE_STONE, RESOURCE_BRICK, RESOURCE_GLASS,	\
	RESOURCE_LOOM, RESOURCE_PAPER }


SCIENCE_GEAR 	= "G"
SCIENCE_COMPASS = "C"
SCIENCE_TABLET 	= "T"

DIRECTION_EAST = "<"
DIRECTION_WEST = ">"
DIRECTION_SELF = "v"

ACTION_PLAYCARD = 0
ACTION_DISCARD	= 1
ACTION_STAGEWONDER	= 2

CARDS_BROWN		= "brown"
CARDS_GREY 		= "grey"
CARDS_YELLOW 	= "yellow"
CARDS_BLUE 		= "blue"
CARDS_RED 		= "red"
CARDS_PURPLE 	= "purple"

def sort_cards(cards, reverse=False):
	return sorted(cards, key=lambda x: x.get_name(), reverse=reverse)


def find_card(cards, name):
	for c in cards:
		if c.get_name() == name:
			return c
	return None
