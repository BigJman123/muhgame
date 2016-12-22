# Player derives from Robot so that we can record and run scripts as the player
class Player(Robot):
  def __init__(self):
    # super(Player, self).__init__("you")
    Robot.__init__(self, "you")
    self.player = True
    self.isare = "are"
    self.verborverbs = ""