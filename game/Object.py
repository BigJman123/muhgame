class Object(Base):
  # name: short name of this thing
  # description: full description
  # fixed: is it stuck or can it be taken

  def __init__(self, name, desc, fixed=False):
    Base.__init__(self, name)
    self.description = desc
    self.fixed = fixed

  def describe(self, observer):
    if isinstance(self.description, str):
      return self.description
    else:
      return self.description(self)