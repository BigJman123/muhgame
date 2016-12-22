# A "location" is a place in the game.
class Location(Lockable):
  # name: short name of this location
  # description: full description
  # contents: things that are in a location
  # exits: ways to get out of a location
  # first_time: is it the first time here?
  # actors: other actors in the location

  def __init__(self, name, description, inonat="in"):
    Lockable.__init__(self, name)
    self.description = description
    self.inonat = inonat
    self.contents = {}
    self.exits = {}
    self.first_time = True
    self.actors = {}

  def title(self, actor):
    preamble = ""
    if (actor != self.game.player):
      preamble = "%s %s %s the " % (actor.name.capitalize(), actor.isare, self.inonat)
    return "        --=( %s%s )=--        " % (preamble, self.name)

  def add_object(self, obj):
    self.contents[obj.name] = obj
    obj.game = self.game
    return obj

  def add_actor(self, actor):
    actor.set_location(self)
    return actor

  def new_object(self, name, desc, fixed=False):
    return self.add_object(Object(name, desc, fixed))

  def description_str(self, d):
    if isinstance(d, (list, tuple)):
      desc = ""
      for dd in d:
        desc += self.description_str(dd)
      return desc
    else:
      if isinstance(d, str):
        return self.game.style_text(d,  DESCRIPTION)
      else:
        return self.description_str(d(self))

  def describe(self, observer, force=False):
    desc = ""   # start with a blank string

    # add the description
    if self.first_time or force:
      desc += self.description_str(self.description)
      self.first_time = False

    if self.contents:
      # try to make a readable list of the things
      contents_description = proper_list_from_dict(self.contents)
      # is it just one thing?
      if len(self.contents) == 1:
        desc += self.game.style_text("\nThere is %s here." % \
                                     contents_description, CONTENTS)
      else:
        desc += self.game.style_text("\nThere are a few things here: %s." % \
                                     contents_description, CONTENTS)
      for k in sorted(self.contents.keys()):
        c = self.contents[k]
        if isinstance(c, Container) and c.is_open():
          desc += c.describe_contents()
                                     
    if self.actors:
      for k in sorted(self.actors.keys()):
        a = self.actors[k]
        if a.health < 0:
          deadornot = "lying here dead as a doornail"
        else:
          deadornot = "here"
        if a != observer:
          desc += self.game.style_text("\n" + add_article(a.describe(a)).capitalize() + \
                                       " " + a.isare + " " + deadornot + ".", CONTENTS)

    return desc

  def find_object(self, actor, name):
    if not name:
      return None
    if self.contents:
      if name in self.contents.keys():
        return self.contents
      for c in self.contents.values():
        if isinstance(c, Container) and c.is_open() and name in c.contents.keys():
          return c.contents
    if name in actor.inventory:
      return actor.inventory
    return None

  def replace_object(self, actor, old_name, new_obj):
    d = self.find_object(actor, old_name)
    if d == None:
      return None
    if not old_name in d.keys():
      return None
    old_obj = d[old_name]
    del d[old_name]
    if new_obj:
      d[new_obj.name] = new_obj
    return old_obj
    
  def add_exit(self, con, way):
    self.exits[ way ] = con

  def go(self, actor, way):
    if not way in self.exits:
      return None
    
    c = self.exits[ way ]

    # first check if the connection is locked
    if not c.try_unlock(actor):
      return None

    # check if the room on the other side is locked        
    if not c.point_b.try_unlock(actor):
      return None

    return c.point_b

  def debug(self):
    for key in self.exits:
      print "exit: %s" % key