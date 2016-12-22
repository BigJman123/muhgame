# Verb is used for passing in an unbound global function to the constructor
class Verb(BaseVerb):
  def __init__(self, function, name = ""):
    BaseVerb.__init__(self, function, name)

  # explicitly pass in self to the unbound function
  def act(self, actor, noun, words):
    return self.function(self.bound_to, actor, noun, words)