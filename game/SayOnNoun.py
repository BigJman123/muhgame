class SayOnNoun(Say):    
  def __init__(self, string, noun, name = ""):
    Say.__init__(self, string, name)
    self.noun = noun

  def act(self, actor, noun, words):
    if self.noun != noun:
      return False
    self.bound_to.game.output(self.string, FEEDBACK)
    return True