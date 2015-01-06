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

from sys import stdin
from common import *
import cards


class Personality:
	def __init__(self):
		pass
	
	def make_choice(self, options):
		pass


class StupidAI(Personality):
	def __init__(self):
		pass
	
	def make_choice(self, options):
		return 0

class Human(Personality):
	def __init__(self):
		pass
	
	def make_choice(self, options):
		return int(stdin.readline())

