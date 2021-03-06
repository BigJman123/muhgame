# Base is a place to put default inplementations of methods that everything
# in the game should support (eg save/restore, how to respond to verbs etc)
class Base(object):
  def __init__(self, name):
    self.game = None
    self.name = name
    self.verbs = {}
    self.phrases = {}
    self.vars = {}

  def flag(self, f):
    if f in self.vars:
      return self.vars[f]
    else:
      return False

  def set_flag(self, f):
    self.vars[f] = True

  def unset_flag(self, f):
    if f in self.vars:
      del self.vars[f]

  def var(self, var):
    if var in self.vars:
      return self.vars[var]
    else:
      return None

  def set_var(self, var, val):
    self.vars[var] = val

  def unset_var(self, var):
    if var in self.vars:
      del self.vars[var]

  def add_verb(self, v):
    self.verbs[' '.join(v.name.split())] = v
    v.bind_to(self)
    return v

  def get_verb(self, verb):
    c = ' '.join(verb.split())
    if c in self.verbs:
       return self.verbs[c]
    else:
      return None

  def add_phrase(self, phrase, f, requirements = []):
    if isinstance(f, BaseVerb):
      f.bind_to(self)
    self.phrases[' '.join(phrase.split())] = (f, set(requirements))

  def get_phrase(self, phrase, things_present):
    phrase = phrase.strip()
    things_present = set(things_present)
    if not phrase in self.phrases:
      return None
    p = self.phrases[phrase]
    if things_present.issuperset(p[1]):
      return p[0]
    return None

  def output(self, text, message_type = 0):
    self.game.output(text, message_type)