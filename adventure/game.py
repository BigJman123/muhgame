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

painting1 = game.new_location(
  "Painting",
"""The painting is of a person screaming. Something seems off about it."""
)

safe1 = game.new_location("Safe",
"""this is a safe""")

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

# CONTAINERS
painting2 = painting1.add_object(Container("painting", "A painting of a man screaming"))

safe2 = safe1.add_object(Container("an old safe", "A very old safe with a four digit lock"))


# CONNECTIONS
game.new_connection("Painting", room, painting1, [FORWARD], [BACK])
game.new_connection("Safe", painting1, safe1,[IN, FORWARD], [OUT, BACK])
game.new_connection("Bookshelf", room, bookshelf, [LEFT], [RIGHT])
game.new_connection("Rug", room, rug, [RIGHT], [LEFT])
game.new_connection("Trapdoor", rug, trapdoor, [RIGHT], [LEFT])
game.new_connection("Cellar", trapdoor, cellar, [RIGHT], [LEFT])


# OBJECTS
key  = safe2.new_object("key", "an old key") 
book = bookshelf.new_object("book", "an old book")

# REQUIREMENTS
safe2.make_requirement(book)
trapdoor.make_requirement(key)

# PHRASE
book.add_phrase("look at book", Say("'19th Century Painters'. You flip through the book and find a page for Edvard Munch. In 1893, Munch painted the famous painting The Scream"))
key.add_phrase("look at key", Say("An old key"))

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