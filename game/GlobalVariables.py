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

  # registered games
registered_games = {}

FEEDBACK = 0
TITLE = 1
DESCRIPTION = 2
CONTENTS = 3
DEBUG = 4

articles = ['a', 'an', 'the']
# some prepositions to recognize indirect objects in prepositional phrases
prepositions = ['aboard', 'about', 'above', 'across', 'after', 'against', 'along'
    'among', 'around', 'at', 'atop', 'before', 'behind', 'below', 'beneath',
    'beside', 'besides', 'between', 'beyond', 'by', 'for', 'from', 'in', 'including'
    'inside', 'into', 'on', 'onto', 'outside', 'over', 'past', 'than' 'through', 'to',
    'toward', 'under', 'underneath',  'onto', 'upon', 'with', 'within']


