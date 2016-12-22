# 
# adventure module
#
# vim: et sw=2 ts=2 sts=2

# for Python3, use:
# import urllib.request as urllib2
import urllib2

import random
import string
import textwrap
import time

# "directions" are all the ways you can describe going some way; 
# they are code-visible names for directions for adventure authors
direction_names = ["NORTH","SOUTH","EAST","WEST","UP","DOWN","RIGHT","LEFT",
                   "IN","OUT","FORWARD","BACK",
                   "NORTHWEST","NORTHEAST","SOUTHWEST","SOUTHEAST"]
direction_list  = [ NORTH,  SOUTH,  EAST,  WEST,  UP,  DOWN,  RIGHT,  LEFT,
                    IN,  OUT,  FORWARD,  BACK,
                    NORTHWEST,  NORTHEAST,  SOUTHWEST,  SOUTHEAST] = \
                    range(len(direction_names))
NOT_DIRECTION = None

# some old names, for backwards compatibility
(NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST) = \
             (NORTHWEST, NORTHEAST, SOUTHWEST, SOUTHEAST)

directions = dir_by_name = dict(zip(direction_names, direction_list))


def define_direction (number, name):
    if name in dir_by_name:
        exit("%s is already defined as %d" % (name, dir_by_name[name]))
    dir_by_name[name] = number

def lookup_dir (name):
    return dir_by_name.get(name, NOT_DIRECTION)

# add lower-case versions of all names in direction_names
for name in direction_names:
    define_direction(dir_by_name[name], name.lower())

# add common aliases:
# maybe the alias mechanism should be a more general
# (text-based?) mechanism that works for any command?!!!
common_aliases = [
    (NORTH, "n"),
    (SOUTH, "s"),
    (EAST, "e"),
    (WEST, "w"),
    (UP, "u"),
    (DOWN, "d"),
    (FORWARD, "fd"),
    (FORWARD, "fwd"),
    (FORWARD, "f"),
    (BACK, "bk"),
    (BACK, "b"),
    (NORTHWEST,"nw"),
    (NORTHEAST,"ne"),
    (SOUTHWEST,"sw"),
    (SOUTHEAST, "se")
]

for (k,v) in common_aliases:
    define_direction(k,v)

# define the pairs of opposite directions
opposite_by_dir = {}

def define_opposite_dirs (d1, d2):
  for dir in (d1, d2):
    opposite = opposite_by_dir.get(dir)
    if opposite is not None:
      exit("opposite for %s is already defined as %s" % (dir, opposite))
  opposite_by_dir[d1] = d2
  opposite_by_dir[d2] = d1

opposites = [(NORTH, SOUTH),
             (EAST, WEST),
             (UP, DOWN),
             (LEFT, RIGHT), 
             (IN, OUT),
             (FORWARD, BACK),
             (NORTHWEST, SOUTHEAST),
             (NORTHEAST, SOUTHWEST)]

for (d1,d2) in opposites:
  define_opposite_dirs(d1,d2)

def opposite_direction (dir):
  return opposite_by_dir[dir]


# registered games
registered_games = {}

FEEDBACK = 0
TITLE = 1
DESCRIPTION = 2
CONTENTS = 3
DEBUG = 4

class Colors:
  '''
  Colors class:
  reset all colors with colors.reset
  two subclasses fg for foreground and bg for background.
  use as colors.subclass.colorname.
  i.e. colors.fg.red or colors.bg.green
  also, the generic bold, disable, underline, reverse, strikethrough,
  and invisible work with the main class
  i.e. colors.bold
  '''
  reset='\033[0m'
  bold='\033[01m'
  disable='\033[02m'
  underline='\033[04m'
  reverse='\033[07m'
  strikethrough='\033[09m'
  invisible='\033[08m'
  class FG:
    black='\033[30m'
    red='\033[31m'
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    cyan='\033[36m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m'
    lightgreen='\033[92m'
    yellow='\033[93m'
    lightblue='\033[94m'
    pink='\033[95m'
    lightcyan='\033[96m'
  class BG:
    black='\033[40m'
    red='\033[41m'
    green='\033[42m'
    orange='\033[43m'
    blue='\033[44m'
    purple='\033[45m'
    cyan='\033[46m'
    lightgrey='\033[47m'

articles = ['a', 'an', 'the']
# some prepositions to recognize indirect objects in prepositional phrases
prepositions = ['aboard', 'about', 'above', 'across', 'after', 'against', 'along'
    'among', 'around', 'at', 'atop', 'before', 'behind', 'below', 'beneath',
    'beside', 'besides', 'between', 'beyond', 'by', 'for', 'from', 'in', 'including'
    'inside', 'into', 'on', 'onto', 'outside', 'over', 'past', 'than' 'through', 'to',
    'toward', 'under', 'underneath',  'onto', 'upon', 'with', 'within']


# changes "lock" to "a lock", "apple" to "an apple", etc.
# note that no article should be added to proper names;
# For now we'll just assume
# anything starting with upper case is proper.
# Do not add an article to plural nouns.
def add_article (name):
  # simple plural test
  if len(name) > 1 and name[-1] == 's' and name[-2] != 's':
    return name
  # check if there is already an article on the string
  if name.split()[0] in articles:
    return name
  consonants = "bcdfghjklmnpqrstvwxyz"
  vowels = "aeiou"
  if name and (name[0] in vowels):
     article = "an "
  elif name and (name[0] in consonants):
     article = "a "
  else:
     article = ""
  return "%s%s" % (article, name)


def normalize_input(text):
  superfluous = articles +  ['and']
  rest = []
  for word in text.split():
    word = "".join(l for l in word if l not in string.punctuation)
    if word not in superfluous:
      rest.append(word)
  return ' '.join(rest)


def proper_list_from_dict(d):
  names = d.keys()
  buf = []
  name_count = len(names)
  for (i,name) in enumerate(names):
    if i != 0:
      buf.append(", " if name_count > 2 else " ")
    if i == name_count-1 and name_count > 1:
      buf.append("and ")
    buf.append(add_article(name))
  return "".join(buf)