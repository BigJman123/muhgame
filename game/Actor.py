# An actor in the game
class Actor(Base):
  # location
  # inventory
  # moved
  # verbs

  def __init__(self, name):
    Base.__init__(self, name)
    self.health = 0
    self.location = None
    self.allowed_locs = None
    self.inventory = {}
    self.cap_name = name.capitalize()
    self.player = False
    self.isare = "is"
    self.verborverbs = "s"
    self.trades = {}
    # associate each of the known actions with functions
    self.add_verb(BaseVerb(self.act_take1, 'take'))
    self.add_verb(BaseVerb(self.act_take1, 'get'))
    self.add_verb(BaseVerb(self.act_drop1, 'drop'))
    self.add_verb(BaseVerb(self.act_give, 'give'))
    self.add_verb(BaseVerb(self.act_inventory, 'inventory'))
    self.add_verb(BaseVerb(self.act_inventory, 'i'))
    self.add_verb(BaseVerb(self.act_look, 'look'))
    self.add_verb(BaseVerb(self.act_examine1, 'examine'))
    self.add_verb(BaseVerb(self.act_examine1, 'look at'))
    self.add_verb(BaseVerb(self.act_look, 'l'))
    self.add_verb(BaseVerb(self.act_go1, 'go'))
    self.add_verb(BaseVerb(self.act_eat, 'eat'))
    self.add_verb(BaseVerb(self.act_drink, 'drink'))
    self.add_verb(BaseVerb(self.act_open, 'open'))
    self.add_verb(BaseVerb(self.act_list_verbs, 'verbs'))
    self.add_verb(BaseVerb(self.act_list_verbs, 'commands'))

  # terminate
  def terminate(self):
    self.health = -1
    
  # describe ourselves
  def describe(self, observer):
    return self.name

  # establish where we are "now"
  def set_location(self, loc):
    self.game = loc.game # XXX this is a hack do this better
    if not self.player and self.location:
      del self.location.actors[self.name]
    self.location = loc
    self.moved = True
    if not self.player:
      self.location.actors[self.name] = self

  # confine this actor to a list of locations
  def set_allowed_locations(self, locs):
    self.allowed_locs = locs

  # add something to our inventory
  def add_to_inventory(self, thing):
    self.inventory[thing.name] = thing
    return thing

  # remove something from our inventory
  def remove_from_inventory(self, thing):
    return self.inventory.pop(thing.name, None)
    
  # set up a trade
  def add_trade(self, received_obj, returned_obj, verb):
    verb.bind_to(self)
    self.trades[received_obj] = (returned_obj, verb)

  # receive a given object
  def receive_item(self, giver, thing):
    self.add_to_inventory(thing)
    if thing in self.trades.keys():
      (obj, verb) = self.trades[thing]
      verb.act(giver, thing.name, None)
      self.location.contents[obj.name] = obj
      self.remove_from_inventory(obj)

  # give something to another actor
  def act_give(self, actor, noun, words):
    d = actor.location.find_object(actor, noun)
    if not d:
      return False
    thing = d[noun]

    receiver = self
    if words:
      for w in words:
        if w in self.location.actors.keys():
          receiver = self.location.actors[w]
          break

    if not receiver:
      return False

    receiver.receive_item(actor, thing)
    del d[thing.name]
    return True
      
  # move a thing from the current location to our inventory
  def act_take1(self, actor, noun, words):
    if not noun:
      return False
    t = self.location.contents.pop(noun, None)
    if not t:
      for c in self.location.contents.values():
        if isinstance(c, Container) and c.is_open:
          t = c.contents.pop(noun, None)      
    if t:
      self.inventory[noun] = t
      self.output("%s take%s the %s." % (actor.cap_name,
                                         actor.verborverbs,
                                         t.name))
      return True
    else:
      self.output("%s can't take the %s." % (actor.cap_name, noun))
      return False

  # move a thing from our inventory to the current location
  def act_drop1(self, actor, noun, words):
    if not noun:
      return False
    t = self.inventory.pop(noun, None)
    if t:
      self.location.contents[noun] = t
      return True
    else:
      self.output("%s %s not carrying %s." % (self.cap_name, self.isare, add_article(noun)), FEEDBACK)
      return False

  def act_look(self, actor, noun, words):
    self.output(self.location.describe(actor, True))
    return True

  # examine a thing in our inventory or location
  def act_examine1(self, actor, noun, words):
    if not noun:
      return False
    n = None
    if noun in self.inventory:
      n = self.inventory[noun]
    if noun in self.location.contents:
      n = self.location.contents[noun]
    for c in self.location.contents.values():
      if isinstance(c, Container) and c.is_open:
        if noun in c.contents:
          n = c.contents[noun]
    if not n:
      return False
    self.output("You see " + n.describe(self) + ".")
    return True

  # list the things we're carrying
  def act_inventory(self, actor, noun, words):
    msg = '%s %s carrying ' % (self.cap_name, self.isare)
    if self.inventory.keys():
      msg += proper_list_from_dict(self.inventory)
    else:
      msg += 'nothing'
    msg += '.'
    self.output(msg, FEEDBACK)
    return True

  # check/clear moved status
  def check_if_moved(self):
    status = self.moved
    self.moved = False
    return status

  # try to go in a given direction
  def act_go1(self, actor, noun, words):
    if not noun in directions:
      self.output("Don't know how to go '%s'." % noun, FEEDBACK)
      return False
    loc = self.location.go(actor, directions[noun])
    if loc == None:
      self.output("Bonk! %s can't seem to go that way." % self.name, FEEDBACK)
      return False
    else:
      # update where we are
      self.set_location(loc)
      return True

  # eat something
  def act_eat(self, actor, noun, words):
    d = actor.location.find_object(actor, noun)
    if not d:
      return False
    t = d[noun]
    
    if isinstance(t, Food):
      t.consume(actor, noun, words)
    else:
      self.output("%s can't eat the %s." % (actor.name.capitalize(), noun))

    return True

  # drink something
  def act_drink(self, actor, noun, words):
    d = actor.location.find_object(actor, noun)
    if not d:
      return False
    t = d[noun]
    
    if isinstance(t, Drink):
      t.consume(actor, noun, words)
    else:
      self.output("%s can't drink the %s." % (actor.name.capitalize(), noun))

    return True

  # open a Container
  def act_open(self, actor, noun, words):
    if not noun:
      return False
    if not noun in actor.location.contents:
      return False
    
    t = self.location.contents[noun]
    if isinstance(t, Container):
      t.open(actor)
    else:
      self.output("%s can't open the %s." % (actor.name.capitalize(), noun))

    return True

  def act_list_verbs(self, actor, noun, words):
    things = (actor.inventory.values() + actor.location.contents.values() +
       list(actor.location.actors.values()) + [actor.location] + [actor])
    result = set()
    for t in things:
      for v in t.verbs.keys():
        if len(v.split()) > 1:
          result.add('"' + v + '"')
        else:
          result.add(v);
      for v in t.phrases.keys():
        if len(v.split()) > 1:
          result.add('"' + v + '"')
        else:
          result.add(v);
    self.output(textwrap.fill(" ".join(sorted(result))), FEEDBACK)
    return True

  # support for scriptable actors, override these to implement
  def get_next_script_command(self):
    return None

  def set_next_script_command(self, line):
    return True

  def set_next_script_response(self, response):
    return True