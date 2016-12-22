class Food(Consumable):
  def __init__(self, name, desc, verb, replacement = None):
    Consumable.__init__(self, name, desc, verb, replacement)
    self.consume_term = "eat"