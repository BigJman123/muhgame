class Consumable(Object):
  def __init__(self, name, desc, verb, replacement = None):
    Object.__init__(self, name, desc)
    self.verb = verb
    verb.bind_to(self)
    self.consume_term = "consume"
    self.replacement = replacement
    
  def consume(self, actor, noun, words):
    if not actor.location.replace_object(actor, self.name, self.replacement):
      return False
    
    self.output("%s %s%s %s." % (actor.name.capitalize(), self.consume_term,
                                 actor.verborverbs, self.description))
    self.verb.act(actor, noun, words)
    return True