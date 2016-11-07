import random
from advent import *
from advent import Game, Location, Connection, Object, Animal, Robot, Pet, Player, Lockable, Container
from advent import NORTH, SOUTH, EAST, WEST, UP, DOWN, RIGHT, LEFT, IN, OUT, FORWARD, BACK, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST, NOT_DIRECTION

game = Game("Hopefully this works")

#locations
room = game.new_location(
    "Room",
"""This is the room"""
)

painting = game.new_location(
    "Painting",
"""This is the painting"""
)

#containers
safe = painting.add_object(Container
(
"Safe", 
"This is the safe"
))

#connections
game.new_connection("Painting", room, painting, [FORWARD], [BACK])

#objects
key = room.new_object("key", "this is the key")

safe.make_requirement(key)

player = game.new_player(room)

game.run()