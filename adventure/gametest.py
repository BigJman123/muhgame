import random
from advent import *
from advent import Game, Location, Connection, Object, Animal, Robot, Pet, Player, Lockable, Container
from advent import NORTH, SOUTH, EAST, WEST, UP, DOWN, RIGHT, LEFT, IN, OUT, FORWARD, BACK, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST, NOT_DIRECTION

game = Game("test")


# LOCATIONS
room = game.new_location(
    "Room",
"""You are in a room. There is a bookshelf in front of you and a door to your left."""
)

theater = game.new_location(
    "Theater",
"""a home movie theater"""
)

bookshelf1 = game.new_location(
    "Bookshelf",
"""a dusty bookshelf. a book is missing from the shelf. a key is on the shelf."""
)

saferoom = game.new_location(
    "Safe",
"""a small room with a safe"""
)


# CONTAINERS
safe2 = saferoom.add_object(Container("safe", "An old safe"))
dvdplayer = theater.add_object(Container("dvd player", "a dvd player"))


# CONNECTIONS
game.new_connection("Bookshelf", room, bookshelf1, [FORWARD], [BACK])
game.new_connection("Theater", room, theater, [LEFT], [RIGHT])
bookshelf2 = game.new_connection("Safe", bookshelf1, saferoom, [FORWARD], [BACK])


# OBJECTS
book = room.new_object("book", "an old book")
key = bookshelf1.new_object("key", "an old key")
nacho = safe2.new_object("nacho libre", "The last copy of nacho libre on planet earth")


# USE OBJECT
bookshelf2.set_flag('locked')
def pick_lock(game, thing):
    game.output('the shelf moves revealing a hidden room')
    thing.unset_flag('locked')
bookshelf2.add_phrase('replace book', pick_lock, [book])

dvdplayer.set_flag('locked')
def pick_lock(game, thing):
    game.output('the lights dim and nacho libre begins to play on the big screen. NACHOOOOOOOOOOOOOO!')
    thing.unset_flag('locked')
dvdplayer.add_phrase('play movie', pick_lock, [book])


# REQUIREMENTS
safe2.make_requirement(key)
dvdplayer.make_requirement(nacho)

player = game.new_player(room)

test_script = Script("test",
"""
> take book
> go forward
> take key
> replace book
> go forward
> open safe
> take nacho libre
> go back
> go back
> go left
> play movie
> end

""")

player.add_script(test_script)

game.run()