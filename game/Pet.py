# A pet is an actor with free will (Animal) that you can also command to do things (Robot)
class Pet(Robot, Animal):
  def __init__(self, name):
    #super(Pet, self).__init__(name )
    Robot.__init__(self, name)

  def act_autonomously(self, observer_loc):
    if self.leader:
      self.set_location(self.leader.location)
    else:
      self.random_move(observer_loc)