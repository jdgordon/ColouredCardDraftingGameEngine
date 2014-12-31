#!/usr/bin/python

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
