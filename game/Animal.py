# Animals are actors which may act autonomously each turn
class Animal(Actor):
  def __init__(self, name):
    #super(Animal, self).__init__(name )
    Actor.__init__(self, name)
    
  def act_autonomously(self, observer_loc):
    self.random_move(observer_loc)

  def random_move(self, observer_loc):
    if random.random() > 0.2:  # only move 1 in 5 times
      return

    # filter out any locked or forbidden locations
    exits = list()    
    for (d, c) in self.location.exits.items():
      if c.is_locked():
        continue
      if c.point_b.is_locked():
        continue
      if self.allowed_locs and not c.point_b in self.allowed_locs:
        continue
      exits.append((d ,c))
    if not exits:
      return
    (exitDir, exitConn) = random.choice(exits)
    quiet = True
    if self.game.current_actor == self.game.player:
      quiet = False
    if self.game.current_actor.flag('verbose'):
      quiet = False
    if not quiet and self.location == observer_loc:
      self.output("%s leaves the %s, heading %s." % \
                  (add_article(self.name).capitalize(),
                   observer_loc.name,
                   direction_names[exitDir].lower()), FEEDBACK)
    self.act_go1(self, direction_names[exitDir], None)
    if not quiet and self.location == observer_loc:
      self.output("%s enters the %s via the %s." % (add_article(self.name).capitalize(),
                                               observer_loc.name,
                                               exitConn.name), FEEDBACK)