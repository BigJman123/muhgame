import random
from advent import *
from advent import Game, Location, Connection, Object, Animal, Robot, Pet, Player, Lockable, Container
from advent import NORTH, SOUTH, EAST, WEST, UP, DOWN, RIGHT, LEFT, IN, OUT, FORWARD, BACK, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST, NOT_DIRECTION

game = Game("Teh Coolest Game")

room = game.new_location(
  "Room",
"""You wake up in a decrepit room. There are no doors or windows. In front of you, hanging on the wall, is a painting.
To your right is a bookshelf, filled with books. In the corner of the room there is a strange looking rug."""
)

painting = game.new_location(
  "Painting",
"""You walk up to the painting. The painting is of a person screaming. Something seems off about the painting."""
)

# A new container
safe = painting.add_object(Container ("An old safe", "A very old safe with a four digit lock"))

bookshelf = game.new_location(
  "Bookshelf",
"""The bookshelf is covered in dust. One of the books appears to have been used recently"""
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

game.new_connection("Painting", room, painting, [FORWARD], [BACK])
game.new_connection("Safe", painting, safe,[IN, FORWARD], [OUT, BACK])
game.new_connection("Bookshelf", room, bookshelf, [LEFT], [RIGHT])
game.new_connection("Rug", room, rug, [RIGHT], [LEFT])
game.new_connection("Trapdoor", rug, trapdoor, [RIGHT], [LEFT])
game.new_connection("Cellar", trapdoor, cellar, [RIGHT], [LEFT])

safe.new_object("Key",
"""An old key"""
)

# Now let's add a thing, a key, by providing a single word name and a longer
# description.
key  = safe.new_object("key", "an old key") 
book = bookshelf.new_object("book", "an old book")

# And we can make the key required to open the office
safe.make_requirement(book)
trapdoor.make_requirement(key)

# Let's add a special phrase. We can attach this phrase to any object, location or actor,
# and the phrase will trigger only if that object or actor is present or at the given location.
book.add_phrase("look at book", Say("'19th Century Painters'. You flip through the book and find a page for Edvard Munch. In 1893, Munch painted the famous painting The Scream"))
key.add_phrase("look at key", Say("An old key"))

player = game.new_player(room)

game.run()