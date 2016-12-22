# Verb is used for passing in an unbound global function to the constructor
class Verb(BaseVerb):
  def __init__(self, function, name = ""):
    BaseVerb.__init__(self, function, name)

  # explicitly pass in self to the unbound function
  def act(self, actor, noun, words):
    return self.function(self.bound_to, actor, noun, words)


def list_prefix(a, b):  # is a a prefix of b
  if not a:
    return True
  if not b:
    return False
  if a[0] != b[0]:
    return False
  return list_prefix(a[1:], b[1:])


def get_noun(words, things):
  if words[0] in articles:
    if len(words) > 1:
      done = False
      for t in things:
        n = t.name.split()
        if list_prefix(n, words[1:]):
          noun = t.name
          words = words[len(n)+1:]
          done = True
          break
      if not done:
        noun = words[1]
        words = words[2:]
  else:
    done = False
    for t in things:
      n = t.name.split()
      if list_prefix(n, words):
        noun = t.name
        words = words[len(n):]
        done = True
        break
    if not done:
      noun = words[0]
      words = words[1:]
  return (noun, words)