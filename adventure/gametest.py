import random
from advent import *
from advent import Game, Location, Connection, Object, Animal, Robot, Pet, Player, Lockable, Container
from advent import NORTH, SOUTH, EAST, WEST, UP, DOWN, RIGHT, LEFT, IN, OUT, FORWARD, BACK, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST, NOT_DIRECTION

game = Game("test")


# LOCATIONS
room = game.new_location(
    "Room",
"""You are in a room. There is a painting in front of you"""
)

painting1 = game.new_location(
    "Painting",
"""This is a painting"""
)

safe1 = game.new_location(
    "Safe",
"""There is a safe behind the painting. It has a four digit combination lock."""
)


# CONTAINERS
painting2 = painting1.add_object(Container("painting", "An old painting. It looks strange."))

safe2 = painting2.add_object(Container("safe", "An old safe"))


# CONNECTIONS
game.new_connection("Painting", room, painting1, [FORWARD], [BACK])
game.new_connection("Safe", painting1, safe1, [FORWARD], [BACK])


# OBJECTS
key = room.new_object("key", "an old key")


# REQUIREMENTS
safe2.make_requirement(key)

player = game.new_player(room)

game.run()