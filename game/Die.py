class Die(BaseVerb):
  def __init__(self, string, name = ""):
    BaseVerb.__init__(self, None, name)
    self.string = string

  def act(self, actor, noun, words):
    self.bound_to.game.output("%s %s %s" % (actor.name.capitalize(),
                                            actor.isare, self.string), FEEDBACK)
    self.bound_to.game.output("%s %s dead." % (actor.name.capitalize(),
                                               actor.isare), FEEDBACK)
    actor.terminate()
    return True