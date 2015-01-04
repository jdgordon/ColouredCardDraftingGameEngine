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

class Wonder:
	def __init__(self, city, fullname, freeslot):
		self.city = city
		self.fullname = fullname
		self.freeslot = freeslot
		self.side_a = [] # (cost, action)
		self.side_b = [] # (cost, action)
		self.built_stages = 0
	
	def parse_stages(self, text, isSideA=True):
		if isSideA:
			target = self.side_a
		else:
			target = self.side_b
		
		while len(text) >= 2:
			cost = text[0]
			action = text[1]
			target.append((cost, action))
			text = text[2:]
		return True


def read_wonders_file(filename):
	wonders = []
	with open(filename) as f:
		content = f.readlines()
		for line in content:
			if line.startswith("#"):
				continue
			values = line.split(",")
			if len(values) < 5:
				continue
			x = []
			for v in values:
				x.append(v.strip())
			w = Wonder(x[0], x[1], x[2])
			count = int(x[3])
			side_a = x[4:4 + count * 2]
			side_b = x[4 + count * 2:]
			if w.parse_stages(side_a, True) and w.parse_stages(side_b, False):
				wonders.append(w)
	print "Loaded %d wonders" % ( len(wonders))
	return wonders

		
