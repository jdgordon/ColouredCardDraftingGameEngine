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

RESOURCE_MONEY 	= "$"
RESOURCE_WOOD 	= "W"
RESOURCE_ORE 	= "O"
RESOURCE_STONE 	= "S"
RESOURCE_BRICK 	= "B"
RESOURCE_GLASS 	= "G"
RESOURCE_LOOM 	= "L"
RESOURCE_PAPER 	= "P"

# not really a resource, but close enough
RESOURCE_VICTORYPOINT = "V"

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
CARDS_GREEN 	= "green"
CARDS_BLUE 		= "blue"
CARDS_RED 		= "red"
CARDS_PURPLE 	= "purple"

INFOPREFIX_TRADE = "trade"
INFOPREFIX_PROVIDER = "+"


def sort_cards(cards, reverse=False):
	return sorted(cards, key=lambda x: x.get_name(), reverse=reverse)


def find_card(cards, name):
	for c in cards:
		if c.get_name() == name:
			return c
	return None
