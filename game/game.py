import random
from advent import *
from advent import Game, Location, Connection, Object, Animal, Robot, Pet, Player, Lockable, Container
from advent import NORTH, SOUTH, EAST, WEST, UP, DOWN, RIGHT, LEFT, IN, OUT, FORWARD, BACK, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST, NOT_DIRECTION

game = Game("Teh Coolest Game")

# LOCATIONS
room = game.new_location(
  "Room",
"""You wake up in a decrepit room. There are no doors or windows. In front of you, hanging on the wall, is a painting.
To your right is a bookshelf, filled with books. In the corner of the room there is a strange looking rug."""
)

safe1 = game.new_location("Safe",
"""this is a safe""")

bookshelf = game.new_location(
  "Bookshelf",
"""The bookshelf is covered in dust. There is a book sitting open on the shelf"""
)

rug = game.new_location(
  "Old Rug",
"""There is an old rug in the corner of the room. It's placement seems odd."""
)

trapdoor = game.new_location(
  "Trap Door",
"""Underneath the rug you find a trapdoor."""
)

cellar = game.new_location(
  "Cellar",
"""The trap door leads to a dark cellar. Where could it lead?"""
)

# CONTAINERS
safe2 = safe1.add_object(Container("safe", "A very old safe with a four digit lock"))
book = bookshelf.add_object(Container("book", "19th Century Painters"))


# OBJECTS
key  = safe2.new_object("key", "an old key")
combination = book.new_object("combination", "the combination is 1893")

# REQUIREMENTS
safe2.make_requirement(combination)
trapdoor.make_requirement(key)

# PHRASE
book.add_phrase("look at book", Say("'19th Century Painters'. You flip through the book and find a page for Edvard Munch. In 1893, Munch painted the famous painting The Scream"))
key.add_phrase("look at key", Say("An old key"))

# CONNECTIONS
game.new_connection("Safe", room, safe1,[IN, FORWARD], [OUT, BACK])
game.new_connection("Bookshelf", room, bookshelf, [LEFT], [RIGHT])
game.new_connection("Rug", room, rug, [RIGHT], [LEFT])
game.new_connection("Trapdoor", rug, trapdoor, [RIGHT], [LEFT])
game.new_connection("Cellar", trapdoor, cellar, [RIGHT], [LEFT])

# PLAYER
player = game.new_player(room)

# TEST SCRIPT
test_script = Script("test",
"""
> go left
> take book
> go right
> go forward
>
>
>
>
>
>
>
>
>
>
>
>
>
>

""")

player2 = player.add_script(test_script)


# RUN
game.run()