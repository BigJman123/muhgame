class Lockable(Base):
  def __init__(self, name):
    Base.__init__(self, name)
    self.requirements = {}
  
  def make_requirement(self, thing):
    self.requirements[thing.name] = thing
    self.lock()
      
  def lock(self):
    self.set_flag('locked')

  def unlock(self):
    self.unset_flag('locked')

  def is_locked(self):
    return self.flag('locked')
    
  def try_unlock(self, actor):
    # first see if the actor is whitelisted
    if isinstance(self, Location) and actor.allowed_locs:
      if not self in actor.allowed_locs:
        return False

    # now check if we're locked
    if not self.flag('locked'):
      return True
    
    # check if there are any implicit requirements for this object
    if len(self.requirements) == 0:
      self.output("It's locked!")
      return False

    # check to see if the requirements are in the inventory
    if set(self.requirements).issubset(set(actor.inventory)):
      self.output("You use the %s, the %s unlocks" % \
                  (proper_list_from_dict(self.requirements),
                  self.name), FEEDBACK)
      self.unlock()
      return True

    self.output("It's locked! You will need %s." % \
                proper_list_from_dict(self.requirements), FEEDBACK)
    return False