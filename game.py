#!/usr/bin/python
import random

from common import *
from cards import helpers
from players import *


cards = helpers.read_cards_file("card-descriptions.txt")

PLAYERS = 3
age_1 = [c for c in cards if c.age == 1 and c.players <= PLAYERS]
age_2 = [c for c in cards if c.age == 2 and c.players <= PLAYERS]
age_3 = [c for c in cards if c.age == 3 and c.get_colour() != "PURPLE" and c.players <= PLAYERS]
purple = [c for c in cards if c.age == 3 and c.get_colour() == "PURPLE" and c.players <= PLAYERS]


random.shuffle(age_1)
random.shuffle(age_2)
random.shuffle(purple)
age_3 += purple[0 : PLAYERS + 2]
random.shuffle(age_3)


p1 = age_1[0:7] + age_2[0:7] + age_3[0:7]
p2 = age_1[7:14] + age_2[7:14] + age_3[7:14]
p3 = age_1[14:21] + age_2[14:21] + age_3[14:21]

players = []
for i in range(0, PLAYERS):
	players.append(Players.Player("player %d" % (i + 1)))

p = players[0]
p.tableau += [cards[1], cards[3], helpers.find_card(cards, "glassworks")]
print p.tableau

#print p._find_resource_cards(['W', 'S', 'W'])

print p.buy_card(helpers.find_card(cards, "dispensary"), [helpers.find_card(cards, "forest cave")], [helpers.find_card(cards, "forest cave")])


