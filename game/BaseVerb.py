class BaseVerb(Base):
  def __init__(self, function, name):
    Base.__init__(self, name)
    self.function = function 
    self.bound_to = None
    
  def bind_to(self, obj):
    self.bound_to = obj
    
  def act(self, actor, noun, words):
    result = True
    if not self.function(actor, noun, None):
      result = False
    # treat 'verb noun1 and noun2..' as 'verb noun1' then 'verb noun2'
    # treat 'verb noun1, noun2...' as 'verb noun1' then 'verb noun2'
    # if any of the nouns work on the verb consider the command successful,
    # even if some of them don't
    if words:
      for noun in words:
        if self.function(actor, noun, None):
          result = True
    return result