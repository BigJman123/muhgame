class Say(BaseVerb):
  def __init__(self, string, name = ""):
    BaseVerb.__init__(self, None, name)
    self.string = string

  def act(self, actor, noun, words):
    self.bound_to.game.output(self.string, FEEDBACK)
    return True