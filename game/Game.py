# The Game: container for hero, locations, robots, animals etc.
class Game(Base):
  def __init__(self, name="bwx-adventure"):
    Base.__init__(self, name)
    self.objects = {}
    self.fresh_location = False
    self.player = None
    self.current_actor = None
    self.location_list = []
    self.robots = {}
    self.animals = {}
    global _devtools
    self.devtools = _devtools
    self.devtools.set_game(self)
    self.http_output = False
    self.http_text = ""
    self.done = False

  def set_name(self, name):
    self.name = name

  # add a bidirectional connection between points A and B
  def add_connection(self, connection):
    connection.game = self
    if isinstance(connection.way_ab, (list, tuple)):
      for way in connection.way_ab:
        connection.point_a.add_exit(connection, way)
    else:
      connection.point_a.add_exit(connection, connection.way_ab)

    # this is messy, need a better way to do this
    reverse_connection = Connection(connection.name,
                                    connection.point_b,
                                    connection.point_a,
                                    connection.way_ba,
                                    connection.way_ab)
    reverse_connection.game = self
    if isinstance(connection.way_ba, (list, tuple)):
      for way in connection.way_ba:
        connection.point_b.add_exit(reverse_connection, way)
    else:
      connection.point_b.add_exit(reverse_connection, connection.way_ba)
    return connection

  def new_connection(self, *args):
    return self.add_connection(Connection(*args))

  def connect(self, place_a, place_b, way_ab, way_ba=None):
    """An easier-to use version of new_connection. It generates a
    connection name automatically from the two location names and also
    allows the second direction argument to be omitted.  If the second
    direction is omitted, it defaults to the opposite of the first
    direction."""
    name = place_a.name + "_to_" + place_b.name
    return self.new_connection(name, place_a, place_b, way_ab, way_ba)


  # add another location to the game
  def add_location(self,  location):
    location.game = self
    self.location_list.append(location)
    return location

  def new_location(self, *args):
    return self.add_location(Location(*args))

  # add an actor to the game
  def add_actor(self, actor):
    actor.game = self

    if isinstance(actor, Player):
      self.player = actor

    if isinstance(actor, Animal):
      self.animals[actor.name] = actor

    if isinstance(actor, Robot):
      self.robots[actor.name] = actor

    return actor

  def new_player(self, location):
    self.player = Player()
    self.add_actor(self.player)
    self.player.set_location(location)
    return self.player

  def if_flag(self, flag, s_true, s_false, location = None):
    return lambda loc: (s_false, s_true)[flag in (location or loc).vars]

  def if_var(self, v, value, s_true, s_false, location = None):
    return lambda loc: (s_false, s_true)[v in (location or loc).vars and (location or loc).vars[v] == value] 

  def output(self, text, message_type = 0):
    if message_type != DEBUG:
      self.current_actor.set_next_script_response(text)
    self.print_output(text, message_type)

  def style_text(self, text, message_type):
    if False: # trinket.io
      return text

    if self.http_output:
      if (message_type == FEEDBACK):
        text = "<font color='red'>" + text + '</font>'
      if (message_type == TITLE):
        text = "<font color='blue'>" + text + '</font>'
      if (message_type == DESCRIPTION):
        pass
      if (message_type == CONTENTS):
        text = "<font color='green'>" + text + '</font>'
      if (message_type == DEBUG):
        text = "<font color='orange'>" + text + '</font>'
      return text

    if (message_type == FEEDBACK):
      text = Colors.FG.pink + text + Colors.reset
    if (message_type == TITLE):
      text = Colors.FG.yellow + Colors.BG.blue + "\n" + text + Colors.reset
    if (message_type == DESCRIPTION):
      text = Colors.reset + text
    if (message_type == CONTENTS):
      text = Colors.FG.green + text + Colors.reset
    if (message_type == DEBUG):
      text = Colors.bold + Colors.FG.black + Colors.BG.orange + "\n" + text + Colors.reset
    return text

  # overload this for HTTP output
  def print_output(self, text, message_type = 0):
    if self.http_output:
      self.http_text += self.style_text(text, message_type) + "\n"
    else:
      print self.style_text(text, message_type)

  # checks to see if the inventory in the items list is in the user's inventory
  def inventory_contains(self, items):
    if set(items).issubset(set(self.player.inventory.values())):
      return True
    return False

  def entering_location(self, location):
    if (self.player.location == location and self.fresh_location):
        return True
    return False

  def say(self, s):
    return lambda game: game.output(s)

  @staticmethod
  def register(name, fn):
    global registered_games
    registered_games[name] = fn

  @staticmethod
  def get_registered_games():
    global registered_games
    return registered_games

  def run_init(self, update_func = None):
    # reset this every loop so we don't trigger things more than once
    self.fresh_location = False
    self.update_func = update_func
    self.current_actor = self.player
    self.devtools.start()

  def init_scripts(self):
    actor = self.current_actor
    script_name = self.var('script_name')
    if script_name != None:
      self.devtools.debug_output("script_name: " + script_name, 3)
      actor.act_load_file(actor, script_name, None)
      if self.flag('check'):
        actor.act_check_script(actor, script_name, None)
      else:
        actor.act_run_script(actor, script_name, None)

    recording_name = self.var('start_recording')
    if recording_name != None:
      self.devtools.debug_output("recording_name: " + recording_name, 3)
      actor.act_start_recording(actor, recording_name, None)
          
  def run_room(self):
    actor = self.current_actor
    if actor == self.player or actor.flag('verbose'):
      # if the actor moved, describe the room
      if actor.check_if_moved():
        self.output(actor.location.title(actor), TITLE)

        # cache this as we need to know it for the query to entering_location()
        self.fresh_location = actor.location.first_time

        where = actor.location.describe(actor, actor.flag('verbose'))
        if where:
          self.output("")
          self.output(where)
          self.output("")

    # See if the animals want to do anything
    for animal in self.animals.values():
      # first check that it is not dead
      if animal.health >= 0:
        animal.act_autonomously(actor.location)


  def run_step(self, cmd = None):
    self.http_text = ""
    actor = self.current_actor

    # has the developer supplied an update function?
    if self.update_func:
      self.update_func() # call the update function

    # check if we're currently running a script
    user_input = actor.get_next_script_command();
    if user_input == None:
      if cmd != None:
        user_input = cmd
      else:
        # get input from the user
        try:
          self.output("")  # add a blank line
          user_input = raw_input("> ")
        except EOFError:
          return False

    # see if the command is for a robot
    if ':' in user_input:
       robot_name, command = user_input.split(':')
       try:
          actor = self.robots[robot_name]
       except KeyError:
          self.output("I don't know anybot named %s" % robot_name, FEEDBACK)
          return True
    else:
       actor = self.player
       command = user_input

    self.current_actor = actor
                
    # now we're done with punctuation and other superfluous words like articles
    command = normalize_input(command)

    # see if we want to quit
    if command == 'q' or command == 'quit':
      return False

    # give the input to the actor in case it's recording a script
    if not actor.set_next_script_command(command):
      return True

    words = command.split()
    if not words:
      return True

    # following the Infocom convention commands are decomposed into
    # VERB(verb), OBJECT(noun), INDIRECT_OBJECT(indirect).
    # For example: "hit zombie with hammer" = HIT(verb) ZOMBIE(noun) WITH HAMMER(indirect).

    # handle 'tell XXX ... "
    target_name = ""
    if words[0].lower() == 'tell' and len(words) > 2:
      (target_name, words) = get_noun(words[1:], actor.location.actors.values())

    things = actor.inventory.values() + \
      actor.location.contents.values() + \
      actor.location.exits.values() + \
      list(actor.location.actors.values()) + \
      [actor.location] + \
      [actor]

    for c in actor.location.contents.values():
        if isinstance(c, Container) and c.is_open:
          things += c.contents.values()
      
    potential_verbs = []
    for t in things:
      potential_verbs += t.verbs.keys()

    # extract the VERB
    verb = None
    potential_verbs.sort(key=lambda key : -len(key))
    for v in potential_verbs:
      vv = v.split()
      if list_prefix(vv, words):
        verb = v
        words = words[len(vv):]
    if not verb:
      verb = words[0]
      words = words[1:]

    # extract the OBJECT
    noun = None
    if words:
      (noun, words) = get_noun(words, things)

    # extract INDIRECT (object) in phrase of the form VERB OBJECT PREPOSITION INDIRECT
    indirect = None
    if len(words) > 1 and words[0].lower() in prepositions:
      (indirect, words) = get_noun(words[1:], things)

    # first check phrases
    for thing in things:
      f = thing.get_phrase(command, things)
      if f:
        if isinstance(f, BaseVerb):
          if f.act(actor, noun, words):
            return True
        else:
          f(self, thing)
          return True

    # if we have an explicit target of the VERB, do that.
    # e.g. "tell cat eat foo" -> cat.eat(cat, 'food', [])
    if target_name:
      for a in actor.location.actors.values():
        if a.name != target_name:
          continue
        v = a.get_verb(verb)
        if v:
          if v.act(a, noun, words):
            return True
      self.output("Huh? %s %s?" % (target_name, verb), FEEDBACK)
      return True

    # if we have an INDIRECT object, try it's handle first
    # e.g. "hit cat with hammer" -> hammer.hit(actor, 'cat', [])
    if indirect:
      # try inventory and room contents
      things = actor.inventory.values() + actor.location.contents.values()
      for thing in things:
        if indirect == thing.name:
          v = thing.get_verb(verb)
          if v:
            if v.act(actor, noun, words):
              return True
      for a in actor.location.actors.values():
        if indirect == a.name:
          v = a.get_verb(verb)
          if v:
            if v.act(a, noun, words):
              return True

    # if we have a NOUN, try it's handler next
    if noun:
      for thing in things:
        if noun == thing.name:
          v = thing.get_verb(verb)
          if v:
            if v.act(actor, None, words):
              return True
      for a in actor.location.actors.values():
        if noun == a.name:
          v = a.get_verb(verb)
          if v:
            if v.act(a, None, words):
              return True

    # location specific VERB
    v = actor.location.get_verb(verb)
    if v:
      if v.act(actor, noun, words):
        return True

    # handle directional moves of the actor
    if not noun:
      if verb in directions:
        actor.act_go1(actor, verb, None)
        return True

    # general actor VERB
    v = actor.get_verb(verb)
    if v:
      if v.act(actor, noun, words):
        return True

    # not understood
    self.output("Huh?", FEEDBACK)
    return True

  def run(self , update_func = None):
    self.run_init(update_func)
    self.run_room() # just set the stage before we do any scripting
    self.init_scripts() # now we can set up scripts
    while True:
      if self.done:
          return
      self.run_room()
      if self.player.health < 0:
        self.output ("Better luck next time!")
        break
      if not self.run_step():
        break
    self.output("\ngoodbye!\n", FEEDBACK)